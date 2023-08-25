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
        tiles = repository.wall.draw_tile(round_id, player.id, 13)
        player.hand = tiles


def discard_tile(round_id: int, player: Player, tile_id: int):
    repository.player.discard_tile(round_id, player.id, tile_id)
    player.hand = repository.player.fetch_hand(round_id, player.id)
    player.discarded = repository.player.fetch_discarded_tiles(round_id,
                                                               player.id)


def tsumo_tile(round_id: int, player: Player):
    player.hand = repository.player.fetch_hand(round_id, player.id)
    player.discarded = repository.player.fetch_discarded_tiles(round_id,
                                                               player.id)
    tile = repository.wall.draw_tile(round_id, player.id)[0]
    player.tsumo = tile
