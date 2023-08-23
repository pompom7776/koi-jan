from typing import List

from model.player import Player
from model.round import Round
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
