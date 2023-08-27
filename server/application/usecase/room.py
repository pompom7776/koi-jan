import random
from typing import List

from socketio import Server

from model.player import Player
from model.room import Room
import repository.db.room as room_repo
import repository.db.player as player_repo
import interfaces.response.room as emit


def connect(socket_io: Server, socket_id: str):
    emit.connected(socket_io, [socket_id])


def create_room(player_id: int) -> Room:
    def generate_room_number() -> int:
        while True:
            room_number: int = random.randint(1000, 9999)
            # TODO: room_numberを重複しないようにする
            return room_number

    room_number: int = generate_room_number()
    room = room_repo.create_room(room_number, player_id)

    return room


def enter_room(socket_io: Server,
               room_number: int,
               players: List[Player],
               player: Player):
    # TODO: 部屋がない場合に対応
    # TODO: 満席の場合に対応
    # TODO: 既に同じ名前のプレイヤーが入室している場合に対応
    rooms = room_repo.fetch_open_rooms()
    room = next((room for room in rooms if room.number == room_number))
    room_repo.enter_room(room.id, player.id)

    emit.entered_room(socket_io, [player.socket_id], room.number)
    emit.joined_room(socket_io,
                     [p.socket_id for p in players],
                     player.name)


def leave_room(socket_io: Server,
               room_id: int,
               players: List[Player],
               player: Player):
    room_repo.leave_room(room_id, player.id)
    emit.left_room(socket_io,
                   [p.socket_id for p in players],
                   player.name)


def reconnect(socket_io: Server,
              new_socket_id: str,
              old_socket_id: str,
              players: List[Player]):
    player_repo.update_player_socket_id(new_socket_id, old_socket_id)
    emit.reconnected(socket_io, [new_socket_id], new_socket_id)
    emit.players_info(socket_io,
                      [new_socket_id],
                      [p.name for p in players])


def ready(socket_io: Server,
          players: List[Player],
          room_id: int,
          player: Player):
    room_repo.ready_room(room_id, player.id)
    emit.readied_game(socket_io,
                      [p.socket_id for p in players],
                      player.name)


def unready(socket_io: Server,
            players: List[Player],
            room_id: int,
            player: Player):
    room_repo.unready_room(room_id, player.id)
    emit.unreadied_game(socket_io,
                        [p.socket_id for p in players],
                        player.name)
