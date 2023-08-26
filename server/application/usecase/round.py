from typing import List
import random

from model.game import Game
from model.player import Player
from model.tile import Tile
from model.round import Round, WINDS
import repository.db.tile as tile_repo
import repository.db.wall as wall_repo
import repository.db.room as room_repo
import repository.db.round as round_repo
import repository.db.draw as draw_repo
import repository.db.discard as discard_repo
import repository.db.call as call_repo


def setup_round(game: Game):
    tiles = tile_repo.fetch_all_tiles()
    random.shuffle(tiles)
    wall = wall_repo.create_wall(tiles)
    players = room_repo.fetch_players_in_room(game.room_id)
    random.shuffle(players)
    dealer = players[0]
    round = round_repo.create_round(game.id, 1, "east", dealer.id, wall.id)
    round.wall_remaining_number = wall.remaining_number
    dora = wall_repo.fetch_dora(wall.id)
    round.dora = dora + [Tile(0, "-", 0, "-")
                         for _ in range(5-wall.dora_number)]
    for wind, player in zip(WINDS, players):
        seat_wind = round_repo.set_seat_wind(round.id, player.id, wind)
        round.seat_winds.append(seat_wind)

    round.current_player_id = dealer.id

    game.round = round


def deal_tiles(players: List[Player], round_id: int):
    for player in players:
        draw_repo.draw_tile(round_id, player.id, 13)
        player.hand = draw_repo.fetch_hand(round_id, player.id)


def discard_tile(round_id: int, player: Player, tile_id: int) -> Tile:
    discard_repo.discard_tile(round_id, player.id, tile_id)
    tile = tile_repo.fetch_tile(tile_id)

    return tile


def tsumo_tile(round_id: int, player: Player):
    tile = draw_repo.draw_tile(round_id, player.id)[0]
    player.tsumo = tile


def get_round(round_id: int) -> Round:
    round = round_repo.fetch_round(round_id)
    wall = wall_repo.fetch_wall(round.wall_id)
    round.wall_remaining_number = wall.remaining_number
    round.seat_winds = None
    round.dora = None
    round.current_player_id = None

    return round


def get_round_id_by_room_id(room_id: int) -> int:
    round_id = round_repo.fetch_round_id_by_room_id(room_id)
    return round_id


def get_next_player_id(round_id: int, player_id: int) -> int:
    current_wind = round_repo.fetch_wind_by_player_id(round_id,
                                                      player_id)
    wind_index = WINDS.index(current_wind)
    if wind_index == len(WINDS) - 1:
        next_wind = WINDS[0]
    else:
        next_wind = WINDS[wind_index + 1]
    next_player_id = round_repo.fetch_player_id_by_wind(round_id, next_wind)

    return next_player_id


def get_hand(round_id: int, player: Player):
    player.hand = draw_repo.fetch_hand(round_id, player.id)


def get_discarded(round_id: int, player: Player):
    player.discarded = discard_repo.fetch_discarded_tiles(round_id, player.id)


def get_call(round_id: int, player: Player):
    player.call = call_repo.fetch_call(round_id, player.id)


def pon(round_id: str, caller: Player):
    tile_id, player_id = discard_repo.fetch_latest_discarded_tile(round_id)
    tile = tile_repo.fetch_tile(tile_id)
    call_id = call_repo.call(round_id, "pon", caller.id,
                             player_id, tile_id)
    call_tile_ids = [t.id for t in caller.hand
                     if t.suit == tile.suit and t.rank == tile.rank][:2]
    call_tile_ids.append(tile_id)
    for call_tile_id in call_tile_ids:
        caller.hand = list(filter(lambda t: t.id != call_tile_id, caller.hand))
        call_repo.call_tile(call_id, call_tile_id)


def kan(round_id: str, caller: Player):
    tile_id, player_id = discard_repo.fetch_latest_discarded_tile(round_id)
    tile = tile_repo.fetch_tile(tile_id)
    call_id = call_repo.call(round_id, "kan", caller.id,
                             player_id, tile_id)
    call_tile_ids = [t.id for t in caller.hand
                     if t.suit == tile.suit and t.rank == tile.rank][:3]
    call_tile_ids.append(tile_id)
    for call_tile_id in call_tile_ids:
        caller.hand = list(filter(lambda t: t.id != call_tile_id, caller.hand))
        call_repo.call_tile(call_id, call_tile_id)
