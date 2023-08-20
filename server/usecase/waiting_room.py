from model.player import Player
import repository


def reconnect(new_socket_id: str,
              old_socket_id: str) -> Player:
    repository.player.update_player_socket_id(old_socket_id, new_socket_id)


def get_players(socket_id: str):
    player = repository.player.fetch_player_by_socket_id(socket_id)
    room = repository.room.fetch_open_room_by_player_id(player.id)
    players = repository.room.fetch_players_in_room(room.id)
    player_names = [p.name for p in players]

    return player_names
#
#
# def set_ready(socket_id: str) -> Player:
#     player = repository.player.fetch_player_by_socket_id(socket_id)
#     room = repository.room.fetch_open_room_by_player_id(player.id)
#     repository.room.ready_room(room.id, player.socket_id)
#
#     return player
#
#
# def cancel_ready(players: List[Player], socket_id: str) -> Player:
#     player: Player = next((player for player in players
#                            if player.socket_id == socket_id),
#                           None)
#     if player is None:
#         return None
#
#     player.ready = False
#
#     return player
#
#
# def leave_game(rooms: List[Room],
#                players: List[Player],
#                socket_id: str) -> Tuple[Player, str]:
#     player_index = next(
#         (i for i, player in enumerate(players)
#          if player.socket_id == socket_id),
#         None)
#     player = players[player_index]
#     if player is None:
#         return None, "プレイヤーが見つかりません"
#
#     room: Room = next((room for room in rooms
#                        if room.room_id == player.room_id),
#                       None)
#     if room is None:
#         return None, "部屋が見つかりません"
#
#     room.players = [p for p in room.players if player.socket_id != socket_id]
#     del players[player_index]
#
#     return player, ""
