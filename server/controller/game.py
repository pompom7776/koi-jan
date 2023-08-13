from typing import List

import eventlet

import usecase.game
import usecase.utils
import presenter.presenter as presenter
from model.room import Room
from model.player import Player, Action
from model.hand import TileFromPlayer


def set(socket_io, rooms: List[Room], players: List[Player]):
    @socket_io.on("run_game")
    def on_run_game(socket_id: str, room_id_str: str):
        room_id: int = int(room_id_str)
        room = usecase.utils.find_room_by_id(rooms, room_id)
        usecase.game.setup(room)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

        while room.table.round < 5:
            while True:
                if room.current_player in room.skip_players:
                    usecase.game.update_next_current_player(
                        room,
                        room.current_player
                    )
                elif room.flag.tsumo:
                    usecase.game.tsumo(room)
                    socket_io.emit("update_game_info",
                                   presenter.room_to_dict(room),
                                   room=room.room_id)

                    player: Player = usecase.utils.find_player_by_id(
                        players, room.current_player
                    )

                    if player.is_riichi:
                        player.action.riichi = False
                        socket_io.emit("update_action",
                                       player.action.__dict__,
                                       room=player.socket_id)

                        if player.action.tsumo:
                            socket_io.emit("can_tsumo",
                                           player.action.__dict__,
                                           room=room.room_id)
                            # 打牌待機 or ツモアガリ
                            room.wait_event.tsumo.wait()
                            room.wait_event.tsumo = eventlet.event.Event()
                        else:
                            usecase.game.discard_tile(room,
                                                      player,
                                                      player.hand.tsumo.id)
                            socket_io.emit("update_game_info",
                                           presenter.room_to_dict(room),
                                           room=room.room_id)
                            room.flag.tsumo = True
                    else:
                        socket_io.emit("draw_tile",
                                       player.action.__dict__,
                                       room=player.socket_id)

                        # 打牌待機
                        room.wait_event.tsumo.wait()
                        room.wait_event.tsumo = eventlet.event.Event()

                    usecase.game.update_next_current_player(
                        room,
                        room.current_player
                    )

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)

        usecase.game.discard_tile(room, players, int(tile_id))
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

        if room.waiter.ron is not []:
            for p in room.waiter.ron:
                socket_io.emit("update_action",
                               p.action.__dict__,
                               room=p.socket_id)
                p.wait_event.ron.wait()
                p.wait_event.ron = eventlet.event.Event()

        if room.waiter.pon is [] and room.waiter.kan is []:
            room.flag.tsumo = True
            room.wait_event.tsumo.send()
        else:
            for p in room.waiter.pon:
                socket_io.emit("update_action",
                               p.action.__dict__,
                               room=p.socket_id)
            for p in room.waiter.kan:
                socket_io.emit("update_action",
                               p.action.__dict__,
                               room=p.socket_id)

    @socket_io.on("pon")
    def on_pon(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        from_player = usecase.utils.find_player_by_id(room.players,
                                                      room.tmp_tiles.player_id)

        usecase.game.pon(room, player)
        from_player.discarded_tiles.pop(-1)
        usecase.game.update_next_current_player(room, player.id)

        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)
        socket_io.emit("draw_tile",
                       player.action.__dict__,
                       room=player.socket_id)

    @socket_io.on("skip_pon")
    def on_skip_pon(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        room.flag.tsumo = True
        room.wait_event.tsumo.send()

    @socket_io.on("dai_min_kan")
    def on_dai_min_kan(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        from_player = usecase.utils.find_player_by_id(room.players,
                                                      room.tmp_tiles.player_id)

        usecase.game.dai_min_kan(room, player)
        from_player.discarded_tiles.pop(-1)
        usecase.game.update_next_current_player(room, player.id)

        usecase.game.dead_tsumo(room)
        room.table.wall.dora_num += 1

        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)
        socket_io.emit("draw_tile",
                       player.action.__dict__,
                       room=player.socket_id)

    @socket_io.on("skip_dai_min_kan")
    def on_skip_dai_min_kan(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        room.flag.tsumo = True
        room.wait_event.tsumo.send()

    @socket_io.on("ron")
    def on_ron(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        player.score_info = usecase.game.ron_agari(room, player)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)
        player.wait_event.ron.send()

    @socket_io.on("skip_ron")
    def on_skip_ron(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        player.wait_event.ron.send()

    @socket_io.on("riichi")
    def on_riichi(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        player.is_riichi = not player.is_riichi
        usecase.player.can_riichi(player)
        socket_io.emit("riichi", player.is_riichi, room=socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=socket_id)

    @socket_io.on("tsumo_agari")
    def on_tsumo_agari(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        player.score_info = usecase.game.tsumo_agari(room, player)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

        room.flag.tsumo = True
        room.wait_event.tsumo.send()
