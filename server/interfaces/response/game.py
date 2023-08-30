from dataclasses import asdict
from typing import List

from socketio import Server

from model.room import Room
from model.player import Player
from model.score import Score


def reconnected(socket_io: Server, to: List[str], new_socket_id: str):
    for socket_id in to:
        socket_io.emit("reconnected", new_socket_id, room=socket_id)


def update_game(socket_io: Server, to: List[str], room: Room):
    for socket_id in to:
        socket_io.emit("update_game", asdict(room), room=socket_id)


def update_players(socket_io: Server, to: List[str], players: List[Player]):
    for socket_id in to:
        socket_io.emit("update_players",
                       [asdict(p) for p in players],
                       room=socket_id)


def update_player(socket_io: Server, to: List[str], player: Player):
    for socket_id in to:
        socket_io.emit("update_player",
                       asdict(player),
                       room=socket_id)


def update_remaining_number(socket_io: Server,
                            to: List[str],
                            remaining_number: int):
    for socket_id in to:
        socket_io.emit("update_remaining_number",
                       remaining_number,
                       room=socket_id)


def update_current_player(socket_io: Server,
                          to: List[str],
                          current_player_id: int):
    for socket_id in to:
        socket_io.emit("update_current_player",
                       current_player_id,
                       room=socket_id)


def notice_drew(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_drew", room=socket_id)


def notice_next_draw(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_next_draw", room=socket_id)


def notice_can_pon(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_can_pon", room=socket_id)


def notice_can_kan(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_can_kan", room=socket_id)


def notice_can_ron(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_can_ron", room=socket_id)


def notice_can_riichi(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_can_riichi", room=socket_id)


def notice_can_tsumo(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_can_tsumo", room=socket_id)


def notice_agari(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_agari", room=socket_id)


def notice_end_round(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_end_round", room=socket_id)


def notice_start_vote(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_start_vote", room=socket_id)


def notice_selected(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_selected", room=socket_id)


def notice_unselected(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_unselected", room=socket_id)


def notice_end_vote(socket_io: Server, to: List[str]):
    for socket_id in to:
        socket_io.emit("notice_end_vote", room=socket_id)
