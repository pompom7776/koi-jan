from typing import List, Tuple

from model.player import Player
from model.room import Room


def reconnect(players: List[Player],
              socket_id: str,
              old_socket_id: str) -> Player:
    player: Player = next((player for player in players
                           if player.socket_id == old_socket_id),
                          None)
    if player is None:
        return None

    player.socket_id = socket_id

    return player


def set_ready(players: List[Player], socket_id: str) -> Player:
    player: Player = next((player for player in players
                           if player.socket_id == socket_id),
                          None)
    if player is None:
        return None

    player.ready = True

    return player


def cancel_ready(players: List[Player], socket_id: str) -> Player:
    player: Player = next((player for player in players
                           if player.socket_id == socket_id),
                          None)
    if player is None:
        return None

    player.ready = False

    return player


def leave_game(rooms: List[Room],
               players: List[Player],
               socket_id: str) -> Tuple[Player, str]:
    player_index = next(
        (i for i, player in enumerate(players)
         if player.socket_id == socket_id),
        None)
    player = players[player_index]
    if player is None:
        return None, "プレイヤーが見つかりません"

    room: Room = next((room for room in rooms
                       if room.room_id == player.room_id),
                      None)
    if room is None:
        return None, "部屋が見つかりません"

    room.players = [p for p in room.players if player.socket_id != socket_id]
    del players[player_index]

    return player, ""
