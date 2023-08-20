from socketio import Server

import usecase.room
import usecase.player
import presenter.response.room as emit


def set(socket_io: Server):
    @socket_io.on("create_room")
    def on_create_room(socket_id: str, player_name: str):
        # if player_name == "":
        #     message: str = "名前を入力してください"
        #     emit.notify_error(socket_io, [socket_id], message)
        #     return
        player = usecase.player.register_player(player_name, socket_id)
        room = usecase.room.create_room(player.id)
        usecase.room.enter_room(room.number, player.id)

        emit.entered_room(socket_io, [socket_id], room.number)

    @socket_io.on("enter_room")
    def on_enter_room(socket_id: str, player_name: str, room_number_str: str):
        room_number = int(room_number_str)
        player = usecase.player.register_player(player_name, socket_id)
        usecase.room.enter_room(room_number, player.id)
        players = usecase.room.get_players_in_room(room_number)

        emit.entered_room(socket_io, [socket_id], room_number)
        emit.joined_room(socket_io,
                         [p.socket_id for p in players],
                         player_name)

    @socket_io.on("connect_waiting_room")
    def on_connect_waiting_room(new_socket_id: str, old_socket_id: str):
        usecase.room.reconnect(new_socket_id, old_socket_id)
        player_names = usecase.room.get_players(new_socket_id)

        emit.reconnected(socket_io, [new_socket_id])
        emit.players_info(socket_io, [new_socket_id], player_names)

    @socket_io.on("ready_game")
    def on_ready_game(socket_id: str):
        player = usecase.room.ready(socket_id)
        room = usecase.room.get_room_by_player_id(player.id)
        players = usecase.room.get_players_in_room(room.number)

        emit.readied_room(socket_io,
                          [p.socket_id for p in players],
                          player.name)

    @socket_io.on("unready_game")
    def on_unready_game(socket_id: str):
        player = usecase.room.unready(socket_id)
        room = usecase.room.get_room_by_player_id(player.id)
        players = usecase.room.get_players_in_room(room.number)

        emit.unreadied_room(socket_io,
                            [p.socket_id for p in players],
                            player.name)
