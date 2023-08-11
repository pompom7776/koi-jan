def on_waiting_room(socket_io, rooms, players):
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

    @socket_io.on("get_players")
    def on_get_players(socket_id: str, rid: str):
        room_id = int(rid)
        members = [player.name for player in players
                   if player.room_id == room_id]

        socket_io.emit("players_info", members, room=socket_id)

    @socket_io.on("startGame")
    def on_start_game(socket_id: str, rid: str):
        # hostがゲーム開始ボタンを押したら、roomIDの人全員がそのリンクに飛ぶ
        room_id = int(rid)
        socket_io.emit("started", room=room_id)

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
