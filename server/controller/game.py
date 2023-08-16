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
            print(f"log : start {room.table.round} round")
            while True:
                if (len(room.table.wall.tiles) == 68
                        or room.flag.agari_num >= 3):
                    print(f"log : end {room.table.round} round")
                    socket_io.emit("update_game_info",
                                   presenter.room_to_dict(room),
                                   room=room.room_id)
                    socket_io.emit("end_round", room=room.room_id)

                    room.wait_event.vote.wait()
                    room.wait_event.vote = eventlet.event.Event()

                    usecase.game.next_round(room)
                    socket_io.emit("update_game_info",
                                   presenter.room_to_dict(room),
                                   room=room.room_id)
                    break

                if room.current_player in room.skip_players:
                    print("log : skip " +
                          str({next((p.name for p in room.players
                                     if p.id == room.current_player))}))
                    usecase.game.update_next_current_player(
                        room,
                        room.current_player
                    )
                elif room.flag.tsumo:
                    print("log : tsumo " +
                          str({next((p.name for p in room.players
                                     if p.id == room.current_player))}))
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
                            print("log : discard(riichi) " +
                                  str({
                                      next((p.name for p in room.players
                                            if p.id == room.current_player))
                                  }))
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

                    print("log : update before " +
                          str({next((p.name for p in room.players
                                     if p.id == room.current_player))}))
                    usecase.game.update_next_current_player(
                        room,
                        room.current_player
                    )
                    print("log : update after " +
                          str({next((p.name for p in room.players
                                     if p.id == room.current_player))}))

    @ socket_io.on("discard_tile")
    def on_discard_tile(socket_id: str, tile_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = next(
            (room for room in rooms if room.room_id == player.room_id),
            None)

        print(f"log : discard {player.name}, tile->{tile_id}")
        usecase.game.discard_tile(room, player, int(tile_id))
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

        if room.waiter.ron != []:
            for p in room.waiter.ron:
                print(f"log : can ron {p.name}")
                socket_io.emit("update_action",
                               p.action.__dict__,
                               room=p.socket_id)
                p.wait_event.ron.wait()
                p.wait_event.ron = eventlet.event.Event()

        if room.waiter.pon is None and room.waiter.kan is None:
            room.flag.tsumo = True
            room.wait_event.tsumo.send()
        else:
            if room.waiter.pon and room.waiter.pon.id not in room.skip_players:
                print(f"log : can pon {room.waiter.pon.name}")
                socket_io.emit("update_action",
                               room.waiter.pon.action.__dict__,
                               room=room.waiter.pon.socket_id)
            if room.waiter.kan and room.waiter.kan.id not in room.skip_players:
                print(f"log : can kan {room.waiter.kan.name}")
                socket_io.emit("update_action",
                               room.waiter.kan.action.__dict__,
                               room=room.waiter.kan.socket_id)

    @ socket_io.on("pon")
    def on_pon(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        from_player = usecase.utils.find_player_by_id(room.players,
                                                      room.tmp_tiles.player_id)

        print(f"log : pon {player.name}")
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

    @ socket_io.on("skip_pon")
    def on_skip_pon(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        print(f"log : skip pon {player.name}")
        room.flag.tsumo = True
        room.wait_event.tsumo.send()

    @ socket_io.on("dai_min_kan")
    def on_dai_min_kan(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        from_player = usecase.utils.find_player_by_id(room.players,
                                                      room.tmp_tiles.player_id)

        print(f"log : kan {player.name}")
        usecase.game.dai_min_kan(room, player)
        from_player.discarded_tiles.pop(-1)
        usecase.game.update_next_current_player(room, player.id)

        print(f"log : tsumo(dead) {player.name}")
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

    @ socket_io.on("skip_dai_min_kan")
    def on_skip_dai_min_kan(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        print(f"log : skip kan {player.name}")
        room.flag.tsumo = True
        room.wait_event.tsumo.send()

    @ socket_io.on("ron")
    def on_ron(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        print(f"log : ron {player.name}")
        player.score_info = usecase.game.ron_agari(room, player)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)
        player.wait_event.ron.send()

    @ socket_io.on("skip_ron")
    def on_skip_ron(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)
        room.tmp_tiles = TileFromPlayer()
        player.action = Action()
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        print(f"log : skip ron {player.name}")
        player.wait_event.ron.send()

    @ socket_io.on("riichi")
    def on_riichi(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        player.is_riichi = not player.is_riichi
        print(f"log : riichi {player.name}, {player.is_riichi}")
        usecase.player.can_riichi(player)
        socket_io.emit("riichi", player.is_riichi, room=socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=socket_id)

    @ socket_io.on("tsumo_agari")
    def on_tsumo_agari(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        print(f"log : tsumo agari {player.name}")
        player.score_info = usecase.game.tsumo_agari(room, player)
        socket_io.emit("update_action",
                       player.action.__dict__,
                       room=player.socket_id)
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

        room.flag.tsumo = True
        room.wait_event.tsumo.send()

    @ socket_io.on("close_score_result")
    def on_close_score_result(socket_id: str):
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        socket_io.emit("vote_start", room=player.room_id)

    @ socket_io.on("select_tile")
    def on_select_tile(socket_id: str, tile_id_str: str):
        tile_id = int(tile_id_str)
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        tiles = usecase.hand.get_all_tiles(player.hand)
        tile = next((t for t in tiles if t.id == tile_id))
        selected_tile = next((t for t in player.selected_tiles
                              if t.id == tile_id), None)
        if selected_tile is None:
            player.selected_tiles.append(tile)
            socket_io.emit("selected", room=socket_id)
            socket_io.emit("update_game_info",
                           presenter.room_to_dict(room),
                           room=room.room_id)

    @ socket_io.on("cancel_tile")
    def on_cancel_tile(socket_id: str, tile_id_str: str):
        tile_id = int(tile_id_str)
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        player.selected_tiles = [t for t in player.selected_tiles
                                 if t.id != tile_id]
        socket_io.emit("update_game_info",
                       presenter.room_to_dict(room),
                       room=room.room_id)

    @ socket_io.on("vote")
    def on_vote(socket_id: str, player_id_str: str):
        player_id = int(player_id_str)
        player = usecase.utils.find_player_by_socket_id(players, socket_id)
        room = usecase.utils.find_room_by_id(rooms, player.room_id)

        target_player = usecase.utils.find_player_by_id(players, player_id)
        target_player.voted += 1
        room.votes += 1

        if room.votes == 4:
            for p in room.players:
                p.score = p.round_score * (p.voted + 1)
            room.votes = 0
            room.wait_event.vote.send()
