import random
from typing import List

from model.room import Game
from model.player import Player
from model.round import WINDS
from model.tile import Tile
import repository.game
import repository.tile
import repository.wall
import repository.room
import repository.round


def setup_game(room_id: int) -> Game:
    game = repository.game.create_game(room_id)
    tiles = repository.tile.fetch_all_tiles()
    random.shuffle(tiles)
    wall = repository.wall.create_wall(tiles)
    players = repository.room.fetch_players_in_room(room_id)
    random.shuffle(players)
    dealer = players[0]
    round = repository.round.create_round(game.id, 1, "east",
                                          dealer.id, wall.id)
    round.wall_remaining_number = wall.remaining_number
    dora = repository.wall.fetch_dora(wall.id)
    round.dora = dora + [Tile(0, "-", 0, "-")
                         for _ in range(5-wall.dora_number)]
    for wind, player in zip(WINDS, players):
        seat_wind = repository.round.set_seat_wind(round.id, player.id, wind)
        round.seat_winds.append(seat_wind)

    round.current_player_id = dealer.id

    game.round = round

    return game


def deal_tiles(players: List[Player], round_id: int):
    for player in players:
        repository.wall.draw_tile(round_id, player.id, 13)
        player.hand = repository.player.fetch_hand(round_id, player.id)


def discard_tile(round_id: int, player: Player, tile_id: int) -> Tile:
    repository.player.discard_tile(round_id, player.id, tile_id)
    tile = repository.tile.fetch_tile(tile_id)

    return tile


def tsumo_tile(round_id: int, player: Player):
    tile = repository.wall.draw_tile(round_id, player.id)[0]
    player.tsumo = tile


def check_pon(player: Player, tile: Tile):
    same_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    if len(same_tiles) >= 2 and not player.is_riichi:
        return True
    return False


def check_kan(player: Player, tile: Tile):
    same_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    if len(same_tiles) >= 3 and not player.is_riichi:
        return True
    return False


def pon(round_id: str, caller: Player):
    tile_id, player_id = repository.round.fetch_latest_discarded_tile(round_id)
    tile = repository.tile.fetch_tile(tile_id)
    call_id = repository.player.call(round_id, "pon", caller.id,
                                     player_id, tile_id)
    call_tile_ids = [t.id for t in caller.hand
                     if t.suit == tile.suit and t.rank == tile.rank][:2]
    call_tile_ids.append(tile_id)
    for call_tile_id in call_tile_ids:
        caller.hand = list(filter(lambda t: t.id != call_tile_id, caller.hand))
        repository.player.call_tile(call_id, call_tile_id)


def kan(round_id: str, caller: Player):
    tile_id, player_id = repository.round.fetch_latest_discarded_tile(round_id)
    tile = repository.tile.fetch_tile(tile_id)
    call_id = repository.player.call(round_id, "kan", caller.id,
                                     player_id, tile_id)
    call_tile_ids = [t.id for t in caller.hand
                     if t.suit == tile.suit and t.rank == tile.rank][:3]
    call_tile_ids.append(tile_id)
    for call_tile_id in call_tile_ids:
        caller.hand = list(filter(lambda t: t.id != call_tile_id, caller.hand))
        repository.player.call_tile(call_id, call_tile_id)
