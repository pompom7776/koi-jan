from typing import List
import random

from socketio import Server

from model.room import Room
from model.player import Player
from model.tile import Tile
from model.round import WINDS
import application.utils as utils
import repository.db.tile as tile_repo
import repository.db.wall as wall_repo
import repository.db.round as round_repo
import repository.db.draw as draw_repo
import repository.db.discard as discard_repo
import repository.db.call as call_repo
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


def deal_tiles(socket_io: Server, room: Room):
    for player in room.players:
        draw_repo.draw_tile(room.game.round.id, player.id, 13)
        player.hand = draw_repo.fetch_hand(room.game.round.id, player.id)
    emit.update_players(socket_io,
                        [p.socket_id for p in room.players],
                        room.players)
    emit.notice_next_draw(socket_io,
                          [p.socket_id for p in room.players
                           if p.id == room.game.round.dealer_id])


def update_current_player(socket_io: Server,
                          round_id: int,
                          players: List[Player],
                          player_id: int):
    current_wind = round_repo.fetch_wind_by_player_id(round_id, player_id)
    next_wind = utils.get_next_wind(current_wind)
    next_player_id = round_repo.fetch_player_id_by_wind(round_id,
                                                        next_wind)
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
                 tile_id: int) -> Tile:
    discard_repo.discard_tile(round_id, player.id, tile_id)
    tile = tile_repo.fetch_tile(tile_id)

    player.hand = draw_repo.fetch_hand(round_id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round_id, player.id)
    player.call = call_repo.fetch_call(round_id, player.id)
    emit.update_player(socket_io, [p.socket_id for p in players], player)

    none_call_flags = []
    for p in players:
        p.hand = draw_repo.fetch_hand(round_id, p.id)
        p.discarded = discard_repo.fetch_discarded_tiles(round_id, p.id)
        can_pon = utils.check_pon(p, tile)
        can_kan = utils.check_kan(p, tile)
        if can_pon:
            emit.notice_can_pon(socket_io, [p.socket_id])
        if can_kan:
            emit.notice_can_kan(socket_io, [p.socket_id])
        none_call_flags.append(not any([can_pon, can_kan]))
    if all(none_call_flags):
        update_current_player(socket_io, round_id, players, player.id)


def tsumo_tile(socket_io: Server,
               round_id: int,
               players: List[Player],
               player: Player):
    player.hand = draw_repo.fetch_hand(round_id, player.id)
    player.discarded = discard_repo.fetch_discarded_tiles(round_id, player.id)
    player.call = call_repo.fetch_call(round_id, player.id)
    tile = draw_repo.draw_tile(round_id, player.id)[0]
    player.tsumo = tile
    emit.update_player(socket_io, [p.socket_id for p in players], player)
    emit.notice_drew(socket_io, [player.socket_id])


def call(socket_io: Server,
         round_id: str,
         players: List[Player],
         caller: Player,
         call_type: str):
    caller.hand = draw_repo.fetch_hand(round_id, caller.id)
    caller.discarded = discard_repo.fetch_discarded_tiles(round_id, caller.id)
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
