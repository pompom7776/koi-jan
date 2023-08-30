from socketio import Server

import application.usecase.room as room_usecase
import application.usecase.round as round_usecase
import application.utils.player as player_util
import application.utils.room as room_util
import application.utils.game as game_util
import application.utils.round as round_util


def set(socket_io: Server):
    @socket_io.on("connect_game")
    def on_connect_game(new_socket_id: str, old_socket_id: str):
        player = player_util.get_player_by_socket_id(old_socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        room_usecase.reconnect(socket_io,
                               new_socket_id, old_socket_id, players)

    @socket_io.on("setup_round")
    def on_setup_round(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        room.players = player_util.get_players_in_room(room.number)
        room.game = game_util.get_game_by_room_id(room.id)
        round_usecase.setup_round(socket_io, room)
        round_usecase.deal_tiles(socket_io, room)

    @socket_io.on("next_round")
    def on_next_round(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        room.players = player_util.get_players_in_room(room.number)
        room.game = game_util.get_game_by_room_id(room.id)
        round_usecase.next_round(socket_io, room)
        round_usecase.deal_tiles(socket_io, room)

    @socket_io.on("get_round")
    def on_get_round(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        room.players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)
        room.game = game_util.get_game_by_room_id(room.id)
        round_usecase.get_round(socket_io, room, round_id, socket_id)

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: int, is_riichi: bool = False):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.discard_tile(socket_io, round_id, players,
                                   player, tile_id, is_riichi)

    @socket_io.on("draw_tile")
    def on_draw_tile(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)
        round = round_util.get_round(round_id)

        round_usecase.draw_tile(socket_io, round, players, player)

    @socket_io.on("riichi")
    def on_riichi(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.tiles_discarded_during_riichi(socket_io,
                                                    round_id,
                                                    player)

    @socket_io.on("skip")
    def on_skip(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        discard_player_id = player_util.get_latest_discard_player(round_id)

        round_usecase.update_current_player(socket_io, round_id,
                                            players, discard_player_id)

    @socket_io.on("call")
    def on_call(socket_id: str, call_type: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.call(socket_io, round_id, players, player, call_type)

    @socket_io.on("agari")
    def on_agari(socket_id: str, agari_type: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)
        round = round_util.get_round(round_id)

        round_usecase.agari(socket_io, round, players, player, agari_type)

    @socket_io.on("close_result")
    def on_close_result(socket_id: str):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.start_vote(socket_io, round_id, players)

    @socket_io.on("select_tile")
    def on_select_tile(socket_id: str, tile_id: int):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.select_tile(socket_io, round_id, players,
                                  player, tile_id)

    @socket_io.on("cancel_tile")
    def on_cancel_tile(socket_id: str, tile_id: int):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.cancel_tile(socket_io, round_id, players,
                                  player, tile_id)

    @socket_io.on("vote")
    def on_vote(socket_id: str, target_player_id: int):
        player = player_util.get_player_by_socket_id(socket_id)
        room = room_util.get_room_by_player_id(player.id)
        players = player_util.get_players_in_room(room.number)
        round_id = round_util.get_round_id_by_room_id(room.id)

        round_usecase.vote(socket_io, round_id, players,
                           player, target_player_id)
