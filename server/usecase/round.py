from typing import List

from model.player import Player
from model.round import Round, WINDS
import repository.wall
import repository.round


def deal_tiles(players: List[Player], round_id: int):
    for player in players:
        for _ in range(13):
            tile = repository.wall.draw_tile(round_id, player.id)
            player.hand.append(tile)


def get_round(round_id: int) -> Round:
    round = repository.round.fetch_round(round_id)
    wall = repository.wall.fetch_wall(round.wall_id)
    round.wall_remaining_number = wall.remaining_number
    round.seat_winds = None
    round.dora = None
    round.current_player_id = None

    return round


def tsumo_tile(round_id: int, player: Player):
    tile = repository.wall.draw_tile(round_id, player.id)
    player.tsumo = tile


def get_round_id_by_room_id(room_id: int) -> int:
    round_id = repository.round.fetch_round_id_by_room_id(room_id)
    return round_id


def get_next_player_id(round_id: int, player_id: int) -> int:
    current_wind = repository.round.fetch_wind_by_player_id(
        round_id, player_id)
    wind_index = WINDS.index(current_wind)
    if wind_index == len(WINDS) - 1:
        next_wind = WINDS[0]
    else:
        next_wind = WINDS[wind_index + 1]
    next_player_id = repository.round.fetch_player_id_by_wind(round_id,
                                                              next_wind)

    return next_player_id
