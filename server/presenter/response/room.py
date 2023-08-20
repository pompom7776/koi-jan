from typing import List

from socketio import Server


def notify_error(socket_io: Server, to: List[str], message: str):
    for socket_id in to:
        socket_io.emit("notify_error", message, room=socket_id)


def entered_room(socket_io: Server, to: List[str], room_number: int):
    for socket_id in to:
        socket_io.emit("entered_room", room_number, room=socket_id)


def joined_room(socket_io: Server, to: List[str], player_name: str):
    for socket_id in to:
        socket_io.emit("joined_room", player_name, room=socket_id)


def reconnected(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("reconnected", room=socket_id)


def players_info(socket_io: Server, to: List[str], player_names: List[str]):
    for socket_id in to:
        socket_io.emit("players_info", player_names, room=socket_id)
