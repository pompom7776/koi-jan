from typing import List

import usecase.room
from model.room import Room
from model.player import Player


def set(socket_io, rooms: List[Room], players: List[Player]):
    @socket_io.on("create_room")
    def on_create_room(socket_id: str, player_name: str):
        if player_name == "":
            message: str = "名前を入力してください"
            socket_io.emit("notify_error", message, room=socket_id)
            return

        room_id: int = usecase.room.create_room(rooms)
        player: Player = usecase.room.register_player(players,
                                                      socket_id,
                                                      player_name,
                                                      room_id)
        message: str = usecase.room.enter_room(rooms, room_id, player)

        if message is not None:
            socket_io.emit("notify_error", message, room=socket_id)
            return

        socket_io.enter_room(socket_id, room_id)
        socket_io.emit("update_room", room_id, room=socket_id)

    @socket_io.on("join_room")
    def on_join_room(socket_id: str, player_name: str, room_id_str: str):
        room_id: int = int(room_id_str)
        player: Player = usecase.room.register_player(players,
                                                      socket_id,
                                                      player_name,
                                                      room_id)
        message: str = usecase.room.enter_room(rooms, room_id, player)
        if message is not None:
            socket_io.emit("notify_error", message, room=socket_id)
            return

        socket_io.enter_room(socket_id, room_id)
        socket_io.emit("update_room", room_id, room=socket_id)
        socket_io.emit("player_joined", player.name, room=room_id)
