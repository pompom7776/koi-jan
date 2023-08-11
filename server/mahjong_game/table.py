import random
from typing import List

from mahjong_game.tile import Tile
from mahjong_game.wall import Wall


class Table:
    def __init__(self):
        self.round_wind: str = ""
        self.dealer: int = 0
        self.riichi_stick_count: int = 0
        self.point_stick_count: int = 0
        self.wall: Wall = Wall()
        self.dora: List[Tile] = []
        self.round: int = 0
        self.honba: int = 0
        self.seat_winds = {"east": 0, "south": 0, "west": 0, "north": 0}

    def initialize(self, player_ids: List[int]):
        self.round_wind = "east"
        self.dealer = random.choice(player_ids)
        self.riichi_stick_count = 0
        self.point_stick_count = 0
        self.wall.initialize()
        self.wall.shuffle()
        self.dora = []
        for _ in range(5):
            self.dora.append(self.wall.draw_tile())
        for _ in range(9):
            self.wall.dead_tiles.append(self.wall.draw_tile())
        self.round = 1
        self.honba = 0

    def next_round(self, player_ids: List[int]):
        self.round_wind = "east"
        self.dealer = self.update_next_current_player(self.dealer)
        self.riichi_stick_count = 0
        self.point_stick_count = 0
        self.wall.initialize()
        self.wall.shuffle()
        self.dora = []
        for _ in range(5):
            self.dora.append(self.wall.draw_tile())

    def to_dict(self):
        dora = [t.__dict__ for t in self.dora]
        return {
            "round_wind": self.round_wind,
            "dealer": self.dealer,
            "riichi_stick_count": self.riichi_stick_count,
            "point_stick_count": self.point_stick_count,
            "wall_num": self.wall.get_remaining(),
            "dora": dora,
            "round": self.round,
            "honba": self.honba,
            "seat_winds": self.seat_winds,
        }

    def update_next_current_player(self, current_player_id: int):
        current_seat = None
        for seat, _id in self.seat_winds.items():
            if _id == current_player_id:
                current_seat = seat
                break
        if current_seat is None:
            raise ValueError("Invalid current_player ID")

        seat_order = ["east", "south", "west", "north"]
        current_seat_index = seat_order.index(current_seat)
        next_seat_index = (current_seat_index + 1) % len(seat_order)
        next_seat = seat_order[next_seat_index]
        return self.seat_winds[next_seat]
