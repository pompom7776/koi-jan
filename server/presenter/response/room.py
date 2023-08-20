from typing import List

from socketio import Server


def notify_error(socket_io: Server, to: List[str], message: str):
    for socket_id in to:
        socket_io.emit("notify_error", message, room=socket_id)


def entered_room(socket_io: Server, to: List[str], room_number: int):
    for socket_id in to:
        socket_io.emit("enterded_room", room_number, room=socket_id)
