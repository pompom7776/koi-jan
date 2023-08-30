from dataclasses import asdict
from typing import List

from socketio import Server

from model.chat import Chat


def update_chat(socket_io: Server, to: List[str], chats: List[Chat]):
    for socket_id in to:
        socket_io.emit("update_chat",
                       [asdict(chat) for chat in chats],
                       room=socket_id)
