from socketio import Server

import application.usecase.room as room_usecase
import application.usecase.game as game_usecase
import application.usecase.round as round_usecase
import application.utils as utils


def set(socket_io: Server):
    @socket_io.on("connect_game")
    def on_connect_game(new_socket_id: str, old_socket_id: str):
        player = utils.get_player_by_socket_id(old_socket_id)
        room = utils.get_room_by_player_id(player.id)
        players = utils.get_players_in_room(room.number)
        room_usecase.reconnect(socket_io,
                               new_socket_id, old_socket_id, players)

    @socket_io.on("setup_round")
    def on_setup_round(socket_id: str):
        player = utils.get_player_by_socket_id(socket_id)
        room = utils.get_room_by_player_id(player.id)
        room.players = utils.get_players_in_room(room.number)
        room.game = utils.get_game_by_room_id(room.id)
        round_usecase.setup_round(socket_io, room)
        round_usecase.deal_tiles(socket_io, room)

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: id):
        player = utils.get_player_by_socket_id(socket_id)
        room = utils.get_room_by_player_id(player.id)
        players = utils.get_players_in_room(room.number)
        round_id = utils.get_round_id_by_room_id(room.id)

        round_usecase.discard_tile(socket_io,
                                   round_id, players, player, tile_id)

    @socket_io.on("draw_tile")
    def on_draw_tile(socket_id: str):
        player = utils.get_player_by_socket_id(socket_id)
        room = utils.get_room_by_player_id(player.id)
        players = utils.get_players_in_room(room.number)
        round_id = utils.get_round_id_by_room_id(room.id)

        round_usecase.tsumo_tile(socket_io, round_id, players, player)

    @socket_io.on("skipCall")
    def on_skipCall(socket_id: str):
        player = utils.get_player_by_socket_id(socket_id)
        room = utils.get_room_by_player_id(player.id)
        players = utils.get_players_in_room(room.number)
        round_id = utils.get_round_id_by_room_id(room.id)

        round_usecase.update_current_player(socket_io,
                                            round_id, players, player.id)

    @socket_io.on("call")
    def on_call(socket_id: str, call_type: str):
        player = utils.get_player_by_socket_id(socket_id)
        room = utils.get_room_by_player_id(player.id)
        players = utils.get_players_in_room(room.number)
        round_id = utils.get_round_id_by_room_id(room.id)

        round_usecase.call(socket_io, round_id, players, player, call_type)
