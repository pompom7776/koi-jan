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

        game = usecase.game.setup_game(room.id)

        players = usecase.room.get_players_in_room(room.number)
        room.players = players
        room.game = game

        emit.update_game(socket_io, [p.socket_id for p in players], room)

        usecase.round.deal_tiles(players, game.round.id)

        emit.update_players(socket_io, [p.socket_id for p in players], players)

        dealer = next((p for p in players
                       if p.id == room.game.round.dealer_id))
        usecase.round.tsumo_tile(room.game.round.id,
                                 dealer)
        emit.update_players(socket_io, [p.socket_id for p in players], players)
        emit.notice_draw(socket_io, [dealer.socket_id])

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: id):
        player = usecase.player.get_player_by_socket_id(socket_id)
        room = usecase.room.get_room_by_player_id(player.id)
        round_id = usecase.round.get_round_id_by_room_id(room.id)
        usecase.player.discard_tile(round_id, player.id, tile_id)
        players = usecase.room.get_players_in_room(room.number)
        discardeds = []
        for player in players:
            discarded = usecase.player.get_discarded_tiles(round_id, player.id)
            discardeds.append(discarded)

        print(discardeds)
        emit.update_discarded(socket_io,
                              [p.socket_id for p in players],
                              discardeds)
