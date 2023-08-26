from typing import List
import random

from model.player import Player
from model.room import Room
import repository.db.room as room_repo
import repository.db.player as player_repo


def create_room(player_id: int) -> Room:
    def generate_room_number() -> int:
        while True:
            room_number: int = random.randint(1000, 9999)
            # TODO: room_numberを重複しないようにする
            return room_number

    room_number: int = generate_room_number()
    room = room_repo.create_room(room_number, player_id)

    return room


def enter_room(room_number: int, player_id: int):
    # TODO: 部屋がない場合に対応
    # TODO: 満席の場合に対応
    # TODO: 既に同じ名前のプレイヤーが入室している場合に対応
    rooms = room_repo.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    room_repo.enter_room(room.id, player_id)


def leave_room(room_id: int, player_id: int):
    room_repo.leave_room(room_id, player_id)


def get_players_in_room(room_number: int) -> List[Player]:
    rooms = room_repo.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    players = room_repo.fetch_players_in_room(room.id)

    return players


def reconnect(new_socket_id: str,
              old_socket_id: str):
    player_repo.update_player_socket_id(new_socket_id, old_socket_id)


def get_room_by_player_id(player_id: int) -> Room:
    room = room_repo.fetch_open_room_by_player_id(player_id)

    return room


def get_players(socket_id: str):
    player = player_repo.fetch_player_by_socket_id(socket_id)
    room = room_repo.fetch_open_room_by_player_id(player.id)
    players = room_repo.fetch_players_in_room(room.id)
    player_names = [p.name for p in players]

    return player_names


def ready(socket_id: str) -> Player:
    player = player_repo.fetch_player_by_socket_id(socket_id)
    room = room_repo.fetch_open_room_by_player_id(player.id)
    room_repo.ready_room(room.id, player.id)

    return player


def unready(socket_id: str) -> Player:
    player = player_repo.fetch_player_by_socket_id(socket_id)
    room = room_repo.fetch_open_room_by_player_id(player.id)
    room_repo.unready_room(room.id, player.id)

    return player
