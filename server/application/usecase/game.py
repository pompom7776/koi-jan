from typing import List

from socketio import Server

from model.player import Player
import repository.db.game as game_repo
import interfaces.response.room as emit


def setup_game(socket_io: Server, players: List[Player], room_id: int):
    game_repo.create_game(room_id)
    emit.started_game(socket_io, [p.socket_id for p in players])
