from typing import List

from socketio import Server


def reconnected(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("reconnected", room=socket_id)
