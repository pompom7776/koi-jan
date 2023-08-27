from typing import List

from model.player import Player
import repository.db.room as room_repo
import repository.db.player as player_repo


def get_players_in_room(room_number: int) -> List[Player]:
    rooms = room_repo.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    players = room_repo.fetch_players_in_room(room.id)

    return players


def get_player_by_socket_id(socket_id: str) -> Player:
    player = player_repo.fetch_player_by_socket_id(socket_id)

    return player
