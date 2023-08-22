from socketio import Server

import usecase.room
import usecase.player
import usecase.game
import usecase.round
import presenter.response.game as emit


def set(socket_io: Server):
    @socket_io.on("connect_game")
    def on_connect_game(new_socket_id: str, old_socket_id: str):
        usecase.room.reconnect(new_socket_id, old_socket_id)

        emit.reconnected(socket_io, [new_socket_id], new_socket_id)

    @socket_io.on("setup_game")
    def on_setup_game(socket_id: str):
        player = usecase.player.get_player_by_socket_id(socket_id)
        room = usecase.room.get_room_by_player_id(player.id)
        players = usecase.room.get_players_in_room(room.number)
        game = usecase.game.setup_game(room.id)
        room.players = players
        room.game = game

        emit.update_game(socket_io, [p.socket_id for p in players], room)

        usecase.round.deal_tiles(players, game.round.id)

        emit.update_players(socket_io, [p.socket_id for p in players], players)
