from socketio import Server

import application.usecase.reaction as reaction_usecase
import application.utils.player as player_util
import application.utils.room as room_util


def set(socket_io: Server):
    @socket_io.on("send_reaction")
    def on_send_message(socket_id: str, reaction_id: int):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        reaction_usecase.send_reaction(socket_io, room.id, players,
                                       player.id, reaction_id)
