import random

from mahjong_game.game import Game
from mahjong_game.player import Player


def on_room(socket_io, rooms, players):
    def generate_room_id() -> int:
        while True:
            room_id = random.randint(1000, 9999)
            if not any(room.room_id == room_id for room in rooms):
                return room_id

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
        socket_io.emit(
            "update_room", room.get_id_and_playerids(), room=room_id)

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
