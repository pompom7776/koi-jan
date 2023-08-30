from typing import List

from socketio import Server

from model.player import Player
import repository.db.reaction as reaction_repo
import interfaces.response.reaction as emit


def send_reaction(socket_io: Server,
                  room_id: int,
                  players: List[Player],
                  player_id: int,
                  reaction_id: int):
    reaction_repo.send_reaction(room_id, player_id, reaction_id)
    reaction = reaction_repo.fetch_reaction(reaction_id)
    emit.update_reaction(socket_io,
                         [p.socket_id for p in players],
                         reaction)
