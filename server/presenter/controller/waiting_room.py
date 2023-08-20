from socketio import Server

from model.player import Player
import usecase.waiting_room
import presenter.response.waiting_room as emit


def set(socket_io: Server):
    @socket_io.on("reconnect")
    def on_reconnect(new_socket_id: str, old_socket_id: str):
        usecase.waiting_room.reconnect(new_socket_id,
                                       old_socket_id)

        emit.reconnected(socket_io, [new_socket_id])

    @socket_io.on("get_players")
    def on_get_players(socket_id: str, room_id_str: str):
        room_id: int = int(room_id_str)
        members: List[Player] = [player.name for player in players
                                 if player.room_id == room_id]

        socket_io.emit("players_info", members, room=socket_id)

    @socket_io.on("start_game")
    def on_start_game(socket_id: str, room_id_str: str):
        room_id: int = int(room_id_str)
        socket_io.emit("started", room=room_id)

    @socket_io.on("ready_game")
    def on_ready_game(socket_id: str):
        player: Player = usecase.waiting_room.set_ready(players, socket_id)
        if player is None:
            socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
            return

        socket_io.emit("readied", player.name, room=player.room_id)

    @socket_io.on("cancel_game")
    def on_cancel_game(socket_id: str):
        player: Player = usecase.waiting_room.cancel_ready(players, socket_id)
        if player is None:
            socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
            return

        socket_io.emit("canceled", player.name, room=player.room_id)

    @socket_io.on("leave_game")
    def on_leave_game(socket_id: str):
        player, message = usecase.waiting_room.leave_game(players,
                                                          socket_id)

        if player is None:
            socket_io.emit("notify_error", message, room=socket_id)
            return

        socket_io.leave_room(socket_id, player.room_id)
        socket_io.emit("left", player.name, room=player.room_id)
