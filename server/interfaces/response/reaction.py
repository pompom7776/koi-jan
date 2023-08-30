from dataclasses import asdict
from typing import List

from socketio import Server

from model.reaction import Reaction


def update_reaction(socket_io: Server, to: List[str], reaction: Reaction):
    for socket_id in to:
        socket_io.emit("update_reaction", asdict(reaction), room=socket_id)
