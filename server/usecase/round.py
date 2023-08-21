from typing import List

from model.player import Player
import repository.wall


def deal_tiles(players: List[Player], round_id: int):
    for player in players:
        for _ in range(13):
            tile = repository.wall.draw_tile(round_id, player.id)
            player.hand.append(tile)
