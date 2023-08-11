import eventlet
import eventlet.wsgi
import time


from mahjong_game.game import Game
from mahjong_game.hand import TileFromPlayer
from mahjong_game.tile import Tile


def on_game(socket_io, rooms, players):
    @socket_io.on("setting_game")
    def on_setting_game(socket_id: str, rid: str):
        room_id = int(rid)
        room = next(
            (room for room in rooms if room.room_id == room_id),
            None)
        print("-- setup --")
        room.setup_game()
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

        while room.table.round < 5:
            play_round(room)
            room.table.honba += 1
            room.turn = 0
            room.flag.agari = 0
            socket_io.emit("update_game_info",
                           room.to_dict(), room=room.room_id)

    def play_round(room: Game):
        print("-- play round --")
        while True:
            if room.table.wall.get_remaining() == 0:
                socket_io.emit("update_game_info",
                               room.to_dict(), room=room.room_id)

                socket_io.emit("end_round", room=room.room_id)

                room.stop_vote.wait()
                room.stop_vote = eventlet.event.Event()
                print("restart vote")

                room.next_round()
                break

            if room.flag.agari >= 3:
                socket_io.emit("update_game_info",
                               room.to_dict(), room=room.room_id)

                socket_io.emit("end_round", room=room.room_id)

                room.stop_vote.wait()
                room.stop_vote = eventlet.event.Event()
                print("restart vote")

                room.next_round()
                break

            if room.current_player in room.skip_players:
                print("skip-turn")
                room.update_next_current_player(room.current_player)

            elif room.flag.tsumo:
                player = next(
                    (p for p in room.players if p.id == room.current_player))
                room.turn += 1

                room.flag.tsumo = False
                room.tsumo(player.id)
                print("-- tsumo --")
                if player.is_riichi:
                    print("is_riichi")
                    player.action.riichi = False
                    socket_io.emit("update_game_info",
                                   room.to_dict(), room=room.room_id)
                    socket_io.emit("update_action",
                                   player.action.__dict__,
                                   room=player.socket_id)

                    if player.action.tsumo:
                        print("can_tsumo")
                        socket_io.emit("update_game_info",
                                       room.to_dict(), room=room.room_id)
                        socket_io.emit("can_tsumo",
                                       player.action.__dict__,
                                       room=room.room_id)
                        # ツモアガリ or スキップ(discard_tile)
                        room.stop_tsumo.wait()
                        room.stop_tsumo = eventlet.event.Event()
                    else:
                        print("can_not_tsumo")
                        time.sleep(1)
                        room.discard_tile(player, player.hand.tsumo.id)
                        socket_io.emit("update_game_info",
                                       room.to_dict(), room=room.room_id)
                        room.flag.tsumo = True
                else:
                    print("is_not_riichi")
                    socket_io.emit("update_game_info",
                                   room.to_dict(), room=room.room_id)
                    socket_io.emit("draw_tile",
                                   player.action.__dict__,
                                   room=player.socket_id)
                    # 打牌
                    room.stop_tsumo.wait()
                    room.stop_tsumo = eventlet.event.Event()

                print("current-player updated")
                time.sleep(0.1)
                room.update_next_current_player(room.current_player)
            time.sleep(0.5)

    @socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: str):
        print("discard")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        # waiter = 鳴きやロンをできる人
        pon_waiter, ron_waiter, remove_tile = room.discard_tile(player,
                                                                int(tile_id))
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

        if ron_waiter is not None:
            print("can_ron")
            socket_io.emit("update_action",
                           ron_waiter.action.__dict__,
                           room=ron_waiter.socket_id)
            ron_waiter.stop_ron.wait()
            ron_waiter.stop_ron = eventlet.event.Event()

        # 鳴きがない場合
        if pon_waiter is None:
            print("can_not_pon")
            socket_io.emit("update_game_info",
                           room.to_dict(), room=room.room_id)
            room.flag.tsumo = True
            room.stop_tsumo.send()
        else:
            print("can_pon")
            socket_io.emit("update_action",
                           pon_waiter.action.__dict__,
                           room=pon_waiter.socket_id)

    @socket_io.on("pon")
    def on_pon(socket_id: str):
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        from_player = next((p for p in players
                           if p.id == room.tmp_call_from.player_id))
        room.pon(player)
        # ポンをfalseにしたことを通知
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)

        from_player.discarded_tiles.pop(-1)

        # 手番を鳴いた人に変更する
        room.update_current_player(player.id)
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

        # 打牌をさせる
        socket_io.emit("draw_tile",
                       player.action.__dict__,
                       room=player.socket_id)

    @socket_io.on("skip_pon")
    def on_skip_pon(socket_id: str):
        print("skip_pon")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

        room.tmp_call_from = TileFromPlayer()
        player.action.pon = False
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)

        room.flag.tsumo = True
        room.stop_tsumo.send()

    @socket_io.on("ron")
    def on_ron(socket_id: str):
        print("ron-agari")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        player.score_info = room.ron_agari(player)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)

        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)
        # socket_io.emit("winning", score.__dict__, room=room.room_id)

        room.flag.tsumo = True
        room.stop_tsumo.send()

    @socket_io.on("skip_ron")
    def on_skip_ron(socket_id: str):
        print("skip_ron")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

        room.tmp_ron = Tile()
        player.action.ron = False
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)

        room.flag.tsumo = True
        player.stop_ron.send()

    @socket_io.on("riichi")
    def on_riichi(socket_id: str):
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        player.is_riichi = not player.is_riichi
        room.check_riichi_tile(player)
        socket_io.emit("riichi", player.is_riichi, room=socket_id)
        socket_io.emit("update_game_info", room.to_dict(), room=socket_id)

    @socket_io.on("tsumo_agari")
    def on_tsumo_agari(socket_id: str):
        print("tsumo-agari")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        player.score_info = room.tsumo_agari(player)
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        # socket_io.emit("winning", score.__dict__, room=room.room_id)

        room.flag.tsumo = True
        room.stop_tsumo.send()

    @socket_io.on("close_score_result")
    def on_close_score_result(socket_id: str):
        print("close_tile")
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        socket_io.emit("vote_start", room=room.room_id)

    @socket_io.on("select_tile")
    def on_select_tile(socket_id: str, tid: str):
        print("select_tile")
        tile_id = int(tid)
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        print("tile", tile_id)
        print("hand", player.hand.to_dict())
        tiles = player.hand.get_all_tiles()
        tile = next((t for t in tiles if t.id == tile_id), None)
        selected_tile = next(
            (t for t in player.selected_tiles if t.id == tile_id), None)
        if selected_tile is None:
            player.selected_tiles.append(tile)
            socket_io.emit("selected", room=socket_id)
            socket_io.emit("update_game_info",
                           room.to_dict(), room=room.room_id)

    @socket_io.on("cancel_tile")
    def on_cancel_tile(socket_id: str, tid: str):
        print("cancel_tile")
        tile_id = int(tid)
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        print("tile", tile_id)
        print("hand", player.hand.to_dict())
        player.selected_tiles = [tile for tile in player.selected_tiles
                                 if tile.id != tile_id]
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

    @socket_io.on("vote")
    def on_vote(socket_id: str, pid: str):
        player_id = int(pid)
        player = next(
            (player for player in players
             if player.socket_id == socket_id),
            None)
        if player is None:
            return
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)
        if room is None:
            return

        target_player = next(
            (player for player in players
             if player.id == player_id),
            None)
        if target_player is None:
            return
        target_player.voted += 1
        room.votes += 1

        if room.votes == 4:
            print("vote done")
            for p in room.players:
                p.score = p.round_score * (p.voted + 1)
            room.votes = 0
            room.stop_vote.send()
