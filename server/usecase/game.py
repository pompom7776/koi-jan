import random

import usecase.table
import usecase.player
import usecase.utils
from model.player import Player, Action
from model.hand import TileFromPlayer
from model.room import Room, Flag, Waiter, RoomWaitEvent


def setup(room: Room):
    usecase.table.initialize(room.table)
    room.turn = 0
    room.votes = 0
    room.skip_players = []
    room.flag = Flag()
    room.waiter = Waiter()
    room.wait_event = RoomWaitEvent()
    room.tmp_tiles = TileFromPlayer()
    for player in room.players:
        player.action = Action()
    set_players(room)
    deal_tiles(room)


def set_players(room: Room):
    shuffle_players = random.sample(room.players, len(room.players))
    winds = list(room.table.seat_winds.keys())
    for i, player in enumerate(shuffle_players):
        usecase.player.initialize(player)
        if i == 0:
            room.table.dealer = player.id
            room.current_player = player.id
        player.seat_winds = winds[i]
        room.table.seat_winds.__dict__[winds[i]] = player.id


def deal_tiles(room: Room):
    for player in room.players:
        NUM_TILES = 13
        for _ in range(NUM_TILES):
            tile = usecase.wall.draw_tile(room.table.wall)
            player.hand.tiles.append(tile)


def update_next_current_player(room: Room):
    room.current_player = usecase.table.update_next_current_player(
        room.table,
        room.current_player
    )


def tsumo(room: Room):
    room.flag.tsumo = False
    room.turn += 1
    player: Player = usecase.utils.find_player_by_id(
        room.players, room.current_player
    )
    tile = usecase.wall.draw_tile(room.table)
    player.hand.tsumo = tile

    hand_tiles = usecase.hand.get_all_tiles(player.hand)
    shanten = usecase.score.shanten(hand_tiles)
    if player.hand.calls == [] and shanten <= 0:
        player.action.riichi = True

    agari = usecase.score.agari(player.hand,
                                player.hand.tsumo,
                                [],
                                room.table.round_wind,
                                player.seat_wind,
                                True,
                                player.is_riichi)
    if shanten == -1 and agari.__dict__["yaku"] != []:
        player.action.tsumo = True


def discard_tile(room: Room, player: Player, tile_id: int):
    remove_tile = usecase.hand.update_hand(player.hand, tile_id)
    player.discarded_tiles.append(remove_tile)
    player.action = Action()
    room.waiter = Waiter()
    room.tmp_tiles = TileFromPlayer(remove_tile, player.id)
    for p in room.players:
        if p.id != player.id:
            if usecase.player.can_pon(p, remove_tile):
                p.action.pon = True
                room.waiter.pon.append(p)
            if usecase.player.can_kan(p, remove_tile):
                p.action.kan = True
                room.waiter.kan.append(p)
            if usecase.player.can_ron(p, remove_tile, room.table.round_wind):
                p.action.ron = True
                room.waiter.ron.append(p)
