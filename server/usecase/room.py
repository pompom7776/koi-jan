from typing import List, Tuple
import random

from model.room import Room
from model.player import Player


def create_room(rooms: List[Room]) -> int:
    def generate_room_id() -> int:
        while True:
            room_id: int = random.randint(1000, 9999)
            if not any(room.room_id == room_id for room in rooms):
                return room_id

    room_id: int = generate_room_id()
    room: Room = Room(room_id=room_id)
    rooms.append(room)

    return room_id


def register_player(players: List[Player],
                    socket_id: str,
                    player_name: str,
                    room_id: int) -> Player:
    player = Player(socket_id, player_name, room_id)
    players.append(player)
    return player


def enter_room(rooms: List[Room], room_id: int, player: Player) -> str:
    room = next((room for room in rooms if room.room_id == room_id),
                None)
    if room is None:
        return "部屋が見つかりません"
    if len(room.players) > 3:
        return "部屋は満席です"
    if player.name in [p.name for p in room.players]:
        return "同じ名前のプレイヤーが既に入室しています"

    room.players.append(player)

    return None
