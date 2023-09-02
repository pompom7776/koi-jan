from typing import List
import random

from socketio import Server

from model.room import Room
from model.round import Round, SeatWind
from model.player import Player
from model.tile import Tile
from model.round import WINDS
import application.utils.round as round_util
import application.utils.check as check_util
import application.utils.score as score_util
import repository.db.tile as tile_repo
import repository.db.wall as wall_repo
import repository.db.round as round_repo
import repository.db.draw as draw_repo
import repository.db.discard as discard_repo
import repository.db.call as call_repo
import repository.db.agari as agari_repo
import repository.db.riichi as riichi_repo
import repository.db.select as select_repo
import repository.db.vote as vote_repo
import interfaces.response.game as emit


def setup_round(socket_io: Server, room: Room):
    tiles = tile_repo.fetch_all_tiles()
    random.shuffle(tiles)
    wall = wall_repo.create_wall(tiles)
    random.shuffle(room.players)
    dealer = room.players[0]
    round = round_repo.create_round(room.game.id, 1, "east",
                                    dealer.id, wall.id)
    round.wall_remaining_number = wall.remaining_number
    dora = wall_repo.fetch_dora(wall.id)
    round.dora = dora + [Tile(0, "-", 0, "-")
                         for _ in range(5-wall.dora_number)]
    for wind, player in zip(WINDS, room.players):
        seat_wind = round_repo.set_seat_wind(round.id, player.id, wind)
        round.seat_winds.append(seat_wind)

    round.current_player_id = dealer.id

    room.game.round = round

    emit.update_game(socket_io, [p.socket_id for p in room.players], room)


def next_round(socket_io: Server, room: Room):
    tiles = tile_repo.fetch_all_tiles()
    random.shuffle(tiles)
    wall = wall_repo.create_wall(tiles)
    random.shuffle(room.players)
    dealer = room.players[0]
    round_number = round_repo.fetch_round_count(room.game.id) + 1
    if round_number >= 5:
        emit.notice_end_game(socket_io,
                             [p.socket_id for p in room.players])
    round = round_repo.create_round(room.game.id, round_number, "east",
                                    dealer.id, wall.id)
    round.wall_remaining_number = wall.remaining_number
    dora = wall_repo.fetch_dora(wall.id)
    round.dora = dora + [Tile(0, "-", 0, "-")
                         for _ in range(5-wall.dora_number)]
    previous_round_id = round_repo.fetch_previous_round_id(room.game.id)
    for p in room.players:
        wind = round_repo.fetch_wind_by_player_id(previous_round_id, p.id)
        seat_order = ["east", "south", "west", "north"]
        current_seat_index = seat_order.index(wind)
        next_seat_index = (current_seat_index + 1) % len(seat_order)
        next_wind = seat_order[next_seat_index]
        round_repo.set_seat_wind(round.id, p.id, next_wind)
        seat_wind = SeatWind(0, round.id, p.id, next_wind)
        round.seat_winds.append(seat_wind)

    round.current_player_id = dealer.id
    room.game.round = round

    emit.update_game(socket_io, [p.socket_id for p in room.players], room)


def get_round(socket_io: Server, room: Room, round_id: int, socket_id: str):
    round = round_repo.fetch_round(round_id)
    wall = wall_repo.fetch_wall(round.wall_id)
    round.wall_remaining_number = wall.remaining_number
    round.dora = wall_repo.fetch_dora(round.wall_id)
    round.dora = round.dora + [Tile(0, "-", 0, "-")
                               for _ in range(5-wall.dora_number)]
    for p in room.players:
        wind = round_repo.fetch_wind_by_player_id(round_id, p.id)
        seat_wind = SeatWind(0, round_id, p.id, wind)
        round.seat_winds.append(seat_wind)

    round.current_player_id = round_repo.fetch_current_player_id(round_id)
    room.game.round = round

    for p in room.players:
        p.hand = draw_repo.fetch_hand(round_id, p.id)
        p.discarded = discard_repo.fetch_discarded_tiles(round_id, p.id)
        p.call = call_repo.fetch_call(round_id, p.id)

    emit.update_game(socket_io, [socket_id], room)


def deal_tiles(socket_io: Server, room: Room):
    for player in room.players:
        draw_repo.draw_tile(room.game.round.id, player.id, 13)
        player.hand = draw_repo.fetch_hand(room.game.round.id, player.id)
    emit.update_players(socket_io,
                        [p.socket_id for p in room.players],
                        room.players)
    round = room.game.round
    remaining_number = wall_repo.fetch_remaining_number(round.wall_id)
    emit.update_remaining_number(socket_io,
                                 [p.socket_id for p in room.players],
                                 remaining_number)

    emit.notice_next_draw(socket_io,
                          [p.socket_id for p in room.players
                           if p.id == room.game.round.dealer_id])


def update_current_player(socket_io: Server,
                          round_id: int,
                          players: List[Player],
                          player_id: int):
    current_player_id = player_id
    while True:
        current_wind = round_repo.fetch_wind_by_player_id(round_id,
                                                          current_player_id)
        next_wind = round_util.get_next_wind(current_wind)
        next_player_id = round_repo.fetch_player_id_by_wind(round_id,
                                                            next_wind)
        if agari_repo.fetch_agari(round_id, next_player_id):
            current_player_id = next_player_id
        else:
            break

    emit.update_current_player(socket_io,
                               [p.socket_id for p in players],
                               next_player_id)

    emit.notice_next_draw(socket_io,
                          [p.socket_id for p in players
                           if p.id == next_player_id])


def discard_tile(socket_io: Server,
                 round_id: int,
                 players: List[Player],
                 player: Player,
                 tile_id: int,
                 is_riichi: bool):
    round = round_util.get_round(round_id)
    discard_repo.discard_tile(round_id, player.id, tile_id)
    tile = tile_repo.fetch_tile(tile_id)

    if is_riichi:
        riichi_repo.riichi(round_id, player.id, tile_id)

    player.hand = draw_repo.fetch_hand(round_id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round_id, player.id)
    player.call = call_repo.fetch_call(round_id, player.id)
    player.is_riichi = riichi_repo.fetch_riichi(round_id, player.id)
    player.tsumo = None
    emit.update_player(socket_io, [p.socket_id for p in players], player)

    none_call_flags = []
    for p in players:
        if p.id != player.id:
            p.hand = draw_repo.fetch_hand(round_id, p.id)
            p.discarded = discard_repo.fetch_discarded_tiles(round_id, p.id)
            p.call = call_repo.fetch_call(round_id, p.id)
            p.is_riichi = riichi_repo.fetch_riichi(round_id, p.id)
            p.agari = agari_repo.fetch_agari(round_id, p.id)
            seat_wind = round_repo.fetch_wind_by_player_id(round.id, player.id)
            can_pon = check_util.pon(p, tile)
            can_kan = check_util.kan(p, tile)
            can_ron = check_util.ron(p, tile, seat_wind, round.round_wind)
            if can_pon:
                emit.notice_can_pon(socket_io, [p.socket_id])
            if can_kan:
                emit.notice_can_kan(socket_io, [p.socket_id])
            if can_ron:
                emit.notice_can_ron(socket_io, [p.socket_id])
            none_call_flags.append(not any([can_pon, can_kan, can_ron]))
    if all(none_call_flags):
        update_current_player(socket_io, round_id, players, player.id)


def draw_tile(socket_io: Server,
              round: Round,
              players: List[Player],
              player: Player):
    player.hand = draw_repo.fetch_hand(round.id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round.id, player.id)
    player.call = call_repo.fetch_call(round.id, player.id)
    player.is_riichi = riichi_repo.fetch_riichi(round.id, player.id)
    tiles = draw_repo.draw_tile(round.id, player.id)
    if tiles is None:
        emit.notice_end_round(socket_io, [p.socket_id for p in players])
        for p in players:
            p.hand = draw_repo.fetch_hand(round.id, p.id)
            p.discarded = discard_repo.fetch_discarded_tiles(round.id, p.id)
            p.call = call_repo.fetch_call(round.id, p.id)
            p.score = agari_repo.fetch_score(round.id, p.id)
        emit.update_players(socket_io, [p.socket_id for p in players], players)
        return
    else:
        tile = tiles[0]
    player.tsumo = tile
    emit.update_player(socket_io, [p.socket_id for p in players], player)
    remaining_number = wall_repo.fetch_remaining_number(round.wall_id)
    emit.update_remaining_number(socket_io,
                                 [p.socket_id for p in players],
                                 remaining_number)

    seat_wind = round_repo.fetch_wind_by_player_id(round.id, player.id)
    can_tsumo = check_util.tsumo(player, seat_wind, round.round_wind)
    if can_tsumo:
        emit.notice_can_tsumo(socket_io, [player.socket_id])

    if (player.is_riichi and not can_tsumo):
        discard_tile(socket_io, round.id, players,
                     player, player.tsumo.id, False)
    else:
        can_riichi = check_util.riichi(player)
        if can_riichi:
            emit.notice_can_riichi(socket_io, [player.socket_id])

        emit.notice_drew(socket_io, [player.socket_id])


def call(socket_io: Server,
         round_id: str,
         players: List[Player],
         caller: Player,
         call_type: str):
    caller.hand = draw_repo.fetch_hand(round_id, caller.id)
    caller.discarded = discard_repo.fetch_discarded_tiles(round_id, caller.id)
    caller.is_riichi = riichi_repo.fetch_riichi(round_id, caller.id)
    tile_id, player_id = discard_repo.fetch_latest_discarded_tile(round_id)
    tile = tile_repo.fetch_tile(tile_id)

    call_id = call_repo.call(round_id, call_type, caller.id,
                             player_id, tile_id)
    if call_type == "pon":
        call_tile_ids = [t.id for t in caller.hand
                         if t.suit == tile.suit and t.rank == tile.rank][:2]
    elif call_type == "kan":
        call_tile_ids = [t.id for t in caller.hand
                         if t.suit == tile.suit and t.rank == tile.rank][:3]

    call_tile_ids.append(tile_id)
    for call_tile_id in call_tile_ids:
        caller.hand = list(filter(lambda t: t.id != call_tile_id, caller.hand))
        call_repo.call_tile(call_id, call_tile_id)

    caller.call = call_repo.fetch_call(round_id, caller.id)
    emit.update_player(socket_io, [p.socket_id for p in players], caller)
    emit.update_current_player(socket_io,
                               [p.socket_id for p in players],
                               caller.id)
    emit.notice_drew(socket_io, [caller.socket_id])


def agari(socket_io: Server,
          round: Round,
          players: List[Player],
          player: Player,
          agari_type: str):
    player.hand = draw_repo.fetch_hand(round.id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round.id, player.id)
    player.call = call_repo.fetch_call(round.id, player.id)
    player.is_riichi = riichi_repo.fetch_riichi(round.id, player.id)

    if agari_type == "ron":
        tile_id, player_id = discard_repo.fetch_latest_discarded_tile(round.id)
        tile = tile_repo.fetch_tile(tile_id)
        player.hand.append(tile)
        agari_tile = tile

    elif agari_type == "tsumo":
        tile_id, player_id = draw_repo.fetch_latest_draw_tile(round.id)
        player.hand = list(filter(lambda t: t.id != tile_id, player.hand))
        player.tsumo = tile_repo.fetch_tile(tile_id)
        agari_tile = player.tsumo

    agari_repo.agari(round.id, player.id, player_id, tile_id, agari_type)
    emit.notice_agari(socket_io, [p.socket_id for p in players])

    seat_wind = round_repo.fetch_wind_by_player_id(round.id, player.id)
    result = score_util.agari(player, agari_tile, round.dora,
                              seat_wind, round.round_wind)
    agari_id = agari_repo.agari(round.id, player.id, player_id, tile_id, "ron")
    cost = result.cost["main"] + result.cost["additional"]*2
    yaku = [yaku.name for yaku in result.yaku]
    agari_repo.set_score(agari_id, cost, result.han, result.fu, yaku)

    agari_count = agari_repo.fetch_agari_count(round.id)
    if agari_count >= 3:
        emit.notice_end_round(socket_io, [p.socket_id for p in players])
        for p in players:
            p.score = agari_repo.fetch_score(round.id, p.id)
            p.hand = draw_repo.fetch_hand(round.id, p.id)
            p.discarded = discard_repo.fetch_discarded_tiles(round.id, p.id)
            p.call = call_repo.fetch_call(round.id, p.id)
        emit.update_players(socket_io, [p.socket_id for p in players], players)
    else:
        update_current_player(socket_io, round.id, players, player.id)


def tiles_discarded_during_riichi(socket_io: Server,
                                  round_id: int,
                                  player: Player):
    player.hand = draw_repo.fetch_hand(round_id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round_id, player.id)
    player.call = call_repo.fetch_call(round_id, player.id)
    player.is_riichi = riichi_repo.fetch_riichi(round_id, player.id)
    tile_id, _ = draw_repo.fetch_latest_draw_tile(round_id)
    player.hand = list(filter(lambda t: t.id != tile_id, player.hand))
    player.tsumo = tile_repo.fetch_tile(tile_id)

    all_tiles = player.hand[:]
    all_tiles.append(player.tsumo)

    for tile in all_tiles:
        tmp_tiles = list(filter(lambda t: t.id != tile.id, all_tiles))
        shanten = score_util.shanten(tmp_tiles)
        if shanten <= 0:
            tile.can_riichi = True
        else:
            tile.can_riichi = False

    emit.update_player(socket_io, [player.socket_id], player)


def start_vote(socket_io: Server, round_id: int, players: List[Player]):
    emit.notice_start_vote(socket_io, [p.socket_id for p in players])


def select_tile(socket_io: Server,
                round_id: int,
                players: List[Player],
                player: Player,
                tile_id: int):
    selected_tiles = select_repo.fetch_select_tiles(round_id, player.id)

    if tile_id not in [t.id for t in selected_tiles]:
        select_repo.select_tile(round_id, player.id, tile_id)
        emit.notice_selected(socket_io, [player.socket_id])

        for p in players:
            p.selected = select_repo.fetch_select_tiles(round_id, p.id)

            p.hand = draw_repo.fetch_hand(round_id, p.id)
            p.discarded = discard_repo.fetch_discarded_tiles(round_id, p.id)
            p.call = call_repo.fetch_call(round_id, p.id)

        emit.update_players(socket_io,
                            [p.socket_id for p in players],
                            players)


def cancel_tile(socket_io: Server,
                round_id: int,
                players: List[Player],
                player: Player,
                tile_id: int):
    select_repo.delete_tile(round_id, player.id, tile_id)
    emit.notice_unselected(socket_io, [player.socket_id])

    for p in players:
        p.selected = select_repo.fetch_select_tiles(round_id, p.id)

        p.hand = draw_repo.fetch_hand(round_id, p.id)
        p.discarded = discard_repo.fetch_discarded_tiles(round_id, p.id)
        p.call = call_repo.fetch_call(round_id, p.id)

    emit.update_players(socket_io,
                        [p.socket_id for p in players],
                        players)


def vote(socket_io: Server,
         round_id: int,
         players: List[Player],
         player: Player,
         target_player_id):
    vote_repo.vote(round_id, player.id, target_player_id)

    vote_count = vote_repo.fetch_vote_count(round_id)
    if vote_count >= 4:
        emit.notice_end_vote(socket_io, [p.socket_id for p in players])
