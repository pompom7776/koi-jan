import random
from typing import List

import eventlet

from player import Player, Action
from table import Table
from hand import CallTiles, TileFromPlayer
from tile import Tile
import score


class Flag:
    def __init__(self):
        self.tsumo = True
        self.agari = 0


class Game:
    def __init__(self, room_id: int, players: List[Player]):
        self.room_id = room_id
        self.players = players
        self.player_ids = [p.id for p in players]
        self.table: Table = Table()
        self.current_player: id = 0
        self.turn: int = 0

        self.flag: Flag = Flag()
        self.stop_tsumo = eventlet.event.Event()
        self.stop_vote = eventlet.event.Event()
        self.tmp_call_from: TileFromPlayer = TileFromPlayer()
        self.tmp_ron: Tile = Tile()

        self.skip_players = []
        self.votes: int = 0

    def to_dict(self):
        players = [p.to_dict() for p in self.players]
        return {
            "room_id": self.room_id,
            "players": players,
            "table": self.table.to_dict(),
            "current_player": self.current_player,
            "turn": self.turn,
        }

    def get_id_and_playerids(self):
        return {
            "room_id": self.room_id,
            "players": [player.id for player in self.players],
        }

    def setup_game(self):
        self.table.initialize(self.player_ids)
        self.turn = 0
        self.flag = Flag()
        for player in self.players:
            player.action = Action()
        self.tmp_call_from: TileFromPlayer = TileFromPlayer()
        self.tmp_ron: Tile = Tile()
        self.skip_players = []
        self.votes = 0

        shuffle_players = random.sample(self.players, len(self.players))
        for i, player in enumerate(shuffle_players):
            player.initialize()
            if i == 0:
                self.table.dealer = player.id
                self.current_player = player.id
            winds = list(self.table.seat_winds.keys())
            player.seat_wind = winds[i]
            self.table.seat_winds[winds[i]] = player.id

        self.deal_tiles()

    def next_round(self):
        self.table.next_round(self.player_ids)
        self.turn = 0
        self.flag = Flag()
        for player in self.players:
            player.next_round()

        self.tmp_call_from: TileFromPlayer = TileFromPlayer()
        self.tmp_ron: Tile = Tile()

        self.skip_players = []
        self.votes = 0

        self.deal_tiles()

    def tsumo(self, player_id: int):
        player = next((player for player in self.players
                       if player.id == player_id), None)
        tile = self.table.wall.draw_tile()
        player.hand.update_tsumo(tile)

        shanten = score.shanten(player.hand.get_all_tiles())
        if player.hand.calls == []:
            if shanten <= 0:
                player.action.riichi = True
        agari = score.agari(player.hand, player.hand.tsumo, [],
                            self.table.round_wind, player.seat_wind,
                            True, player.is_riichi)
        if shanten == -1 and agari.__dict__["yaku"] != []:
            player.action.tsumo = True

    def dead_tsumo(self, player_id: int):
        player = next((player for player in self.players
                       if player.id == player_id), None)
        tile = self.table.wall.draw_dead_tile()
        player.hand.update_tsumo(tile)

        shanten = score.shanten(player.hand.get_all_tiles())
        if player.hand.calls == []:
            if shanten <= 0:
                player.action.riichi = True
        agari = score.agari(player.hand, player.hand.tsumo, [],
                            self.table.round_wind, player.seat_wind,
                            True, player.is_riichi)
        if shanten == -1 and agari.__dict__["yaku"] != []:
            player.action.tsumo = True

    def pon(self, player: Player):
        call: CallTiles = CallTiles()
        call.type = "pon"
        call.tiles = [t for t in player.hand.tiles
                      if t.name == self.tmp_call_from.tile.name][:2]
        call.tiles.append(self.tmp_call_from.tile)
        call.from_tile = self.tmp_call_from
        player.hand.calls.append(call)
        for tile in call.tiles:
            player.hand.tiles = list(
                filter(lambda t: t.id != tile.id, player.hand.tiles))

        self.tmp_call_from = TileFromPlayer()
        player.action.pon = False
        player.action.kan = False

    def dai_min_kan(self, player: Player):
        call: CallTiles = CallTiles()
        call.type = "dai_min_kan"
        call.tiles = [t for t in player.hand.tiles
                      if t.name == self.tmp_call_from.tile.name][:3]
        call.tiles.append(self.tmp_call_from.tile)
        call.from_tile = self.tmp_call_from
        player.hand.calls.append(call)
        for tile in call.tiles:
            player.hand.tiles = list(
                filter(lambda t: t.id != tile.id, player.hand.tiles))

        self.tmp_call_from = TileFromPlayer()
        player.action.kan = False
        player.action.pon = False

    def discard_tile(self, player: Player, tile_id: int):
        remove_tile = player.hand.update_hand(tile_id)
        player.update_discrded_tiles(remove_tile)
        player.action.riichi = False
        player.action.tsumo = False
        player.action.ron = False
        pon_waiter = None
        kan_waiter = None
        ron_waiter = None
        for p in self.players:
            if p.id != player.id:
                if p.hand.can_pon(remove_tile) and not p.is_riichi:
                    p.action.pon = True
                    pon_waiter = p
                    self.tmp_call_from.player_id = player.id
                    self.tmp_call_from.tile = remove_tile
                if p.hand.can_kan(remove_tile) and not p.is_riichi:
                    p.action.kan = True
                    kan_waiter = p
                    self.tmp_call_from.player_id = player.id
                    self.tmp_call_from.tile = remove_tile
                if self.check_ron(remove_tile, p):
                    ron_waiter = p
                    self.tmp_ron = remove_tile
                    p.action.ron = True
        return pon_waiter, kan_waiter, ron_waiter, remove_tile

    def deal_tiles(self):
        for player in self.players:
            # 最初に配る枚数
            NUM_TILES = 13

            for _ in range(NUM_TILES):
                tile = self.table.wall.draw_tile()
                player.hand.add_tile(tile)

    def update_next_current_player(self, player_id: int):
        self.current_player = self.table.update_next_current_player(
            player_id)

    def update_current_player(self, player_id: int):
        self.current_player = player_id

    def check_riichi_tile(self, player: Player):
        all_tiles = player.hand.get_all_tiles()
        for t in all_tiles:
            tmp_tiles = list(filter(lambda tile: tile.id != t.id, all_tiles))
            shanten = score.shanten(tmp_tiles)
            if shanten <= 0:
                t.can_riichi = True
            else:
                t.can_riichi = False

    def tsumo_agari(self, player: Player):
        score_info: score.Score = score.agari(hand=player.hand,
                                              win_tile=player.hand.tsumo,
                                              dora=self.table.dora[:self.table.dora_num],
                                              round_wind=self.table.round_wind,
                                              seat_wind=player.seat_wind,
                                              is_tsumo=True,
                                              is_riichi=player.is_riichi)

        player.round_score = score_info.cost
        player.action.tsumo = False
        player.action.pon = False
        self.skip_players.append(player.id)
        self.flag.agari += 1

        return score_info

    def check_ron(self, tile: Tile, player: Player) -> bool:
        player.hand.tiles.append(tile)
        agari = score.agari(player.hand, tile, [],
                            self.table.round_wind, player.seat_wind,
                            False, player.is_riichi)
        _ = player.hand.tiles.pop(-1)
        if agari.__dict__["yaku"] != []:
            return True

        return False

    def ron_agari(self, player: Player):
        player.hand.tiles.append(self.tmp_ron)
        score_info: score.Score = score.agari(hand=player.hand,
                                              win_tile=self.tmp_ron,
                                              dora=self.table.dora[:self.table.dora_num],
                                              round_wind=self.table.round_wind,
                                              seat_wind=player.seat_wind,
                                              is_tsumo=False,
                                              is_riichi=player.is_riichi)

        player.round_score = score_info.cost
        player.action.ron = False
        player.action.pon = False
        self.skip_players.append(player.id)
        self.flag.agari += 1

        return score_info

    def get_all_scores(self):
        for player in self.players:
            pass
