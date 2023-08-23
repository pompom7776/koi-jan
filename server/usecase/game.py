import random

from model.room import Game
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
