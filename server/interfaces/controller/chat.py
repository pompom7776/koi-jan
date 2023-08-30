from socketio import Server

import application.usecase.chat as chat_usecase
import application.utils.player as player_util
import application.utils.room as room_util


def set(socket_io: Server):
    @socket_io.on("send_message")
    def on_send_message(socket_id: str, message: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        chat_usecase.send_message(socket_io, room.id, players,
                                  player.id, message)

    @socket_io.on("get_messages")
    def on_get_messages(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)

        chat_usecase.get_messages(socket_io, room.id, player)
