from socketio import Server

import application.usecase.room as room_usecase
import application.usecase.player as player_usecase
import application.usecase.game as game_usecase
import application.utils.player as player_util
import application.utils.room as room_util


def set(socket_io: Server):
    @socket_io.on("connect")
    def on_connect(socket_id, environ):
        room_usecase.connect(socket_io, socket_id)

    @socket_io.on("create_room")
    def on_create_room(socket_id: str, player_name: str):
        player = player_usecase.register_player(player_name, socket_id)
        room = room_usecase.create_room(player.id)
        room_usecase.enter_room(socket_io, room.number, [player], player)

    @socket_io.on("enter_room")
    def on_enter_room(socket_id: str, player_name: str, room_number_str: str):
        room_number = int(room_number_str)
        player = player_usecase.register_player(player_name, socket_id)
        players = player_util.get_players_in_room(room_number)

        room_usecase.enter_room(socket_io, room_number, players, player)

    @socket_io.on("leave_room")
    def on_leave_room(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        room_usecase.leave_room(socket_io, room.id, players, player)

    @socket_io.on("connect_waiting_room")
    def on_connect_waiting_room(new_socket_id: str, old_socket_id: str):
        player = player_util.get_player_by_socket_id(old_socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        room_usecase.reconnect(socket_io,
                               new_socket_id, old_socket_id, players)

    @socket_io.on("ready_game")
    def on_ready_game(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        room_usecase.ready(socket_io, players, room.id, player)

    @socket_io.on("unready_game")
    def on_unready_game(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        room_usecase.unready(socket_io, players, room.id, player)

    @socket_io.on("start_game")
    def on_start_game(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)

        game_usecase.setup_game(socket_io, players, room.id)
