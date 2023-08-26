from socketio import Server

import application.usecase.room as room_usecase
import application.usecase.player as player_usecase
import presenter.response.room as emit


def set(socket_io: Server):
    @socket_io.on("connect")
    def on_connect(socket_id, environ):
        emit.connected(socket_io, [socket_id])

    @socket_io.on("create_room")
    def on_create_room(socket_id: str, player_name: str):
        # if player_name == "":
        #     message: str = "名前を入力してください"
        #     emit.notify_error(socket_io, [socket_id], message)
        #     return
        player = player_usecase.register_player(player_name, socket_id)
        room = room_usecase.create_room(player.id)
        room_usecase.enter_room(room.number, player.id)

        emit.entered_room(socket_io, [socket_id], room.number)

    @socket_io.on("enter_room")
    def on_enter_room(socket_id: str, player_name: str, room_number_str: str):
        room_number = int(room_number_str)
        player = player_usecase.register_player(player_name, socket_id)
        room_usecase.enter_room(room_number, player.id)
        players = room_usecase.get_players_in_room(room_number)

        emit.entered_room(socket_io, [socket_id], room_number)
        emit.joined_room(socket_io,
                         [p.socket_id for p in players],
                         player_name)

    @socket_io.on("leave_room")
    def on_leave_room(socket_id: str):
        player = room_usecase.unready(socket_id)
        room = room_usecase.get_room_by_player_id(player.id)
        room_usecase.leave_room(room.id, player.id)
        players = room_usecase.get_players_in_room(room.number)

        emit.left_room(socket_io,
                       [p.socket_id for p in players],
                       player.name)

    @socket_io.on("connect_waiting_room")
    def on_connect_waiting_room(new_socket_id: str, old_socket_id: str):
        room_usecase.reconnect(new_socket_id, old_socket_id)
        player_names = room_usecase.get_players(new_socket_id)

        emit.reconnected(socket_io, [new_socket_id], new_socket_id)
        emit.players_info(socket_io, [new_socket_id], player_names)

    @socket_io.on("ready_game")
    def on_ready_game(socket_id: str):
        player = room_usecase.ready(socket_id)
        room = room_usecase.get_room_by_player_id(player.id)
        players = room_usecase.get_players_in_room(room.number)

        emit.readied_game(socket_io,
                          [p.socket_id for p in players],
                          player.name)

    @socket_io.on("unready_game")
    def on_unready_game(socket_id: str):
        player = room_usecase.unready(socket_id)
        room = room_usecase.get_room_by_player_id(player.id)
        players = room_usecase.get_players_in_room(room.number)

        emit.unreadied_game(socket_io,
                            [p.socket_id for p in players],
                            player.name)

    @socket_io.on("start_game")
    def on_start_game(socket_id: str):
        player = room_usecase.unready(socket_id)
        room = room_usecase.get_room_by_player_id(player.id)
        players = room_usecase.get_players_in_room(room.number)

        emit.started_game(socket_io, [p.socket_id for p in players])
