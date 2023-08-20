from typing import List

from socketio import Server


def connected(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("connected", room=socket_id)


def notify_error(socket_io: Server, to: List[str], message: str):
    for socket_id in to:
        socket_io.emit("notify_error", message, room=socket_id)


def entered_room(socket_io: Server, to: List[str], room_number: int):
    for socket_id in to:
        socket_io.emit("entered_room", room_number, room=socket_id)


def left_room(socket_io: Server, to: List[str], player_name: str):
    for socket_id in to:
        socket_io.emit("left_room", player_name, room=socket_id)


def joined_room(socket_io: Server, to: List[str], player_name: str):
    for socket_id in to:
        socket_io.emit("joined_room", player_name, room=socket_id)


def reconnected(socket_io: Server, to: List[str], new_socket_id: str):
    for socket_id in to:
        socket_io.emit("reconnected", new_socket_id, room=socket_id)


def players_info(socket_io: Server, to: List[str], player_names: List[str]):
    for socket_id in to:
        socket_io.emit("players_info", player_names, room=socket_id)


def readied_game(socket_io: Server, to: List[str], player_name: str):
    for socket_id in to:
        socket_io.emit("readied_game", player_name, room=socket_id)


def unreadied_game(socket_io: Server, to: List[str], player_name: str):
    for socket_id in to:
        socket_io.emit("unreadied_game", player_name, room=socket_id)


def started_game(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("started_game", room=socket_id)
