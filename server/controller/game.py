from typing import List

import eventlet

import usecase.game
import usecase.utils
import presenter.presenter as presenter
from model.room import Room
from model.player import Player


def set(socket_io, rooms: List[Room], players: List[Player]):
    @socket_io.on("run_game")
    def on_run_game(socket_id: str, room_id_str: str):
        room_id: int = int(room_id_str)
        room = usecase.utils.find_room_by_id(rooms, room_id)
        if room is None:
            socket_io.emit("notify_error", "部屋が見つかりません", room=socket_id)
            return
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

                        # 打牌待機(ツモアガリの場合はスキップ)
                        room.wait_event.tsumo.wait()
                        room.wait_event.tsumo = eventlet.event.Event()

                        if player.action.tsumo:
                            socket_io.emit("can_tsumo",
                                           player.action.__dict__,
                                           room=room.room_id)
                        else:
                            pass

                    else:
                        socket_io.emit("draw_tile",
                                       player.action.__dict__,
                                       room=player.socket_id)

                        # 打牌待機
                        room.wait_event.tsumo.wait()
                        room.wait_event.tsumo = eventlet.event.Event()

                    usecase.game.update_next_current_player(room)

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        if player is None:
            socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            socket_io.emit("notify_error", "部屋が見つかりません", room=socket_id)
            return

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
