import eventlet
import eventlet.wsgi
import random
import time

import socketio

from game import Game
from player import Player
from hand import TileFromPlayer
from tile import Tile

eventlet.monkey_patch()

socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
app = socketio.WSGIApp(socket_io)

rooms = []
players = []


@socket_io.on("connect")
def on_connect(socket_id, environ):
    print(f"connected : {socket_id}")


@socket_io.on("reconnect")
def on_reconnect(socket_id, old_socket_id):
    player = next(
        (player for player in players
         if player.socket_id == old_socket_id),
        None)

    if player is None:
        socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
        return

    player.socket_id = socket_id

    socket_io.leave_room(old_socket_id, player.room_id)
    socket_io.enter_room(socket_id, player.room_id)
    socket_io.emit("reconnected",
                   {"sid": socket_id, "pid": player.id},
                   room=socket_id)
    print(f"reconnected : {old_socket_id} -> {socket_id}")


@socket_io.on("create_room")
def on_create(socket_id: str, player_name: str):
    if player_name == "":
        socket_io.emit("notify_error", "名前を入力してください", room=socket_id)
        return

    room_id = generate_room_id()

    player = Player(socket_id=socket_id, name=player_name, room_id=room_id)
    room = Game(room_id=room_id, players=[player])
    print(f"{player_name} created {room_id}")

    players.append(player)
    rooms.append(room)

    socket_io.enter_room(socket_id, room_id)
    socket_io.emit("update_room", room.get_id_and_playerids(), room=room_id)


def generate_room_id() -> int:
    while True:
        room_id = random.randint(1000, 9999)
        if not any(room.room_id == room_id for room in rooms):
            return room_id


@socket_io.on("join_room")
def on_join(socket_id: str, player_name: str, rid: str):
    if player_name == "":
        socket_io.emit("notify_error", "名前を入力してください", room=socket_id)
        return

    room_id = int(rid)
    room = next(
        (room for room in rooms if room.room_id == room_id),
        None)

    if room is None:
        socket_io.emit("notify_error", "部屋が見つかりません", room=socket_id)
        return

    # 4人目以降を許さないプログラムを書いてください
    if len(room.players) > 3:
        socket_io.emit("notify_error", "満席です", room=socket_id)
        return

    member_names = [p.name for p in room.players]

    # 同じ人が入らないようにプログラムを書いてください
    if player_name in member_names:
        socket_io.emit("notify_error", "同じ名前が既にいます", room=socket_id)
        return

    player = Player(socket_id=socket_id, name=player_name, room_id=room_id)
    players.append(player)
    room.players.append(player)
    print(f"{player_name} joined {room_id}")

    socket_io.enter_room(socket_id, room_id)
    socket_io.emit(
        "update_room", room.get_id_and_playerids(), room=room_id)
    socket_io.emit("player_joined", player.name, room=room_id)


@socket_io.on("get_players")
def on_get_players(socket_id: str, rid: str):
    room_id = int(rid)
    members = [player.name for player in players if player.room_id == room_id]

    socket_io.emit("players_info", members, room=socket_id)


@socket_io.on("readyGame")
# waitongroomから情報を受け取る(playerのname,ready状況)
def on_ready_game(socket_id: str):
    player = next(
        (player for player in players
         if player.socket_id == socket_id),
        None)
    if player is None:
        socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
        return

    player.ready = True

    # room=room_idにplayer.nameを送信する(readied)
    socket_io.emit("readied", player.name, room=player.room_id)


@socket_io.on("cancelGame")
def on_cancel_game(socket_id: str):
    player = next(
        (player for player in players
         if player.socket_id == socket_id),
        None)
    if player is None:
        socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
        return

    player.ready = True

    # room=room_idにplayer.nameを送信する(readied)
    socket_io.emit("canceled", player.name, room=player.room_id)


@socket_io.on("startGame")
def on_start_game(socket_id: str, rid: str):
    # hostがゲーム開始ボタンを押したら、roomIDの人全員がそのリンクに飛ぶ
    room_id = int(rid)
    socket_io.emit("started", room=room_id)


@socket_io.on("getoutGame")
def on_getout_game(socket_id: str):
    player_index = next(
        (i for i, player in enumerate(players)
         if player.socket_id == socket_id),
        None)
    player = players[player_index]
    if player is None:
        socket_io.emit("notify_error", "プレイヤーが見つかりません", room=socket_id)
        return

    room = next(
        (room for room in rooms if room.room_id == player.room_id),
        None)

    if room is None:
        socket_io.emit("notify_error", "部屋が見つかりません", room=socket_id)
        return

    members = room.players
    room.players = [player for player in members
                    if player.socket_id != socket_id]

    del players[player_index]

    socket_io.leave_room(socket_id, player.room_id)
    socket_io.emit("getout", player.name, room=player.room_id)


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
                                   player.action.__dict__, room=room.room_id)
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
    pon_waiter, kan_waiter, ron_waiter, remove_tile = room.discard_tile(player,
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
    if pon_waiter is None and kan_waiter is None:
        print("can_not_meld")
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)
        room.flag.tsumo = True
        room.stop_tsumo.send()
    else:
        print("can_meld")
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


@socket_io.on("dai_min_kan")
def on_dai_min_kan(socket_id: str):
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
    room.dai_min_kan(player)
    # カンをfalseにしたことを通知
    socket_io.emit("update_action",
                   player.action.__dict__,
                   room=player.socket_id)

    from_player.discarded_tiles.pop(-1)
    # 手番を鳴いた人に変更する
    room.update_current_player(player.id)
    socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)
    time.sleep(0.1)

    room.dead_tsumo(player.id)
    room.table.dora_num += 1
    socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)

    # 打牌をさせる
    socket_io.emit("draw_tile",
                   player.action.__dict__,
                   room=player.socket_id)


@socket_io.on("skip_dai_min_kan")
def on_skip_dai_min_kan(socket_id: str):
    print("skip_dai_min_kan")
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
    player.action.kan = False
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
        socket_io.emit("update_game_info", room.to_dict(), room=room.room_id)


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


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
