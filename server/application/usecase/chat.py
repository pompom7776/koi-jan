from typing import List

from socketio import Server

from model.player import Player
import repository.db.chat as chat_repo
import interfaces.response.chat as emit


def send_message(socket_io: Server,
                 room_id: int,
                 players: List[Player],
                 player_id: int,
                 message: str):
    chat_repo.send_message(room_id, player_id, message)
    chats = chat_repo.fetch_chats(room_id)

    emit.update_chat(socket_io,
                     [p.socket_id for p in players],
                     chats)


def get_messages(socket_io: Server, room_id: int, player: Player):
    chats = chat_repo.fetch_chats(room_id)
    emit.update_chat(socket_io, [player.socket_id], chats)
