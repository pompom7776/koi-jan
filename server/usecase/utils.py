from typing import List

from model.tile import Tile
from model.player import Player
from model.room import Room


def sort_tiles_by_id(tiles: List[Tile]):
    return sorted(tiles, key=lambda tile: tile.id)


def find_room_by_id(rooms: List[Room], room_id: int):
    return next((room for room in rooms if room.room_id == room_id), None)


def find_player_by_id(players: List[Player], player_id: int):
    return next((player for player in players
                 if player.id == player_id), None)


def find_player_by_socket_id(players: List[Player], socket_id: str):
    return next((player for player in players
                 if player.socket_id == socket_id), None)
