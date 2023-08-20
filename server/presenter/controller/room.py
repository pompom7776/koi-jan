from socketio import Server

import usecase.room
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

        emit.enterd_room(socket_io, [socket_id], room.number)

    @socket_io.on("enter_room")
    def on_enter_room(socket_id: str, player_name: str, room_number_str: str):
        room_number = int(room_number_str)
        player = usecase.player.register_player(player_name, socket_id)
        usecase.room.enter_room(room_number, player.id)

        emit.entered_room(socket_io, [socket_id], room_number)
