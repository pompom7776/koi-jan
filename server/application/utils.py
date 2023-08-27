from typing import List

from model.player import Player
from model.room import Room
from model.game import Game
from model.round import Round
from model.tile import Tile
from model.round import WINDS
import repository.db.player as player_repo
import repository.db.room as room_repo
import repository.db.game as game_repo
import repository.db.round as round_repo
import repository.db.wall as wall_repo


def get_players_in_room(room_number: int) -> List[Player]:
    rooms = room_repo.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    players = room_repo.fetch_players_in_room(room.id)

    return players


def get_room_by_player_id(player_id: int) -> Room:
    room = room_repo.fetch_open_room_by_player_id(player_id)

    return room


def get_player_by_socket_id(socket_id: str) -> Player:
    player = player_repo.fetch_player_by_socket_id(socket_id)

    return player


def get_game_by_room_id(room_id: int) -> Game:
    game = game_repo.fetch_game(room_id)

    return game


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


def sort_tiles_by_id(tiles):
    return sorted(tiles, key=lambda tile: tile.id)


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


def get_next_wind(current_wind):
    wind_index = WINDS.index(current_wind)
    if wind_index == len(WINDS) - 1:
        next_wind = WINDS[0]
    else:
        next_wind = WINDS[wind_index + 1]

    return next_wind
