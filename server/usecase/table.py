import random
from typing import List

import usecase.wall
from model.table import Table, SeatWindPlayers
from model.player import Player


def initialize(table: Table, players: List[Player]):
    table.round_wind = "east"
    table.dealer = random.choice([player.id for player in players])
    usecase.wall.initialize(table.wall)
    usecase.wall.shuffle(table.wall)
    usecase.wall.set_dead_tiles(table.wall)
    table.round = 1
    table.seat_winds = SeatWindPlayers()


def next_round(table: Table, players: List[Player]):
    table.dealer = update_next_current_player(table, table.dealer)
    usecase.wall.initialize(table.wall)
    usecase.wall.shuffle(table.wall)
    usecase.wall.set_dead_tiles(table.wall)
    table.round += 1


def update_seat_winds(table: Table):
    table.seat_winds(table.seat_winds.north,
                     table.seat_winds.east,
                     table.seat_winds.south,
                     table.seat_winds.west)


def update_next_current_player(table: Table, current_player_id: int):
    current_seat = None
    for seat, p_id in table.seat_winds.__dict__.items():
        if p_id == current_player_id:
            current_seat = seat
            break
    seat_order = list(table.seat_winds.__dict__.keys())
    current_seat_index = seat_order.index(current_seat)
    next_seat_index = (current_seat_index + 1) % len(seat_order)
    next_seat = seat_order[next_seat_index]

    return table.seat_winds[next_seat]
