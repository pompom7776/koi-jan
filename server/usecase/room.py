from typing import List
import random

from model.player import Player
from model.room import Room
import repository.room


def create_room(player_id: int) -> Room:
    def generate_room_number() -> int:
        while True:
            room_number: int = random.randint(1000, 9999)
            # TODO: room_numberを重複しないようにする
            return room_number

    room_number: int = generate_room_number()
    room = repository.room.create_room(room_number, player_id)

    return room


def enter_room(room_number: int, player_id: int):
    # TODO: 部屋がない場合に対応
    # TODO: 満席の場合に対応
    # TODO: 既に同じ名前のプレイヤーが入室している場合に対応
    rooms = repository.room.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    repository.room.enter_room(room.id, player_id)


def get_players_in_room(room_number: int) -> List[Player]:
    rooms = repository.room.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    players = repository.room.fetch_players_in_room(room.id)

    return players
