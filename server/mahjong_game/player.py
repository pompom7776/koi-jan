from typing import List

import eventlet

from mahjong_game.hand import Hand
from mahjong_game.tile import Tile
from mahjong_game.score import Score


class Action:
    def __init__(self):
        self.riichi: bool = False
        self.chi: bool = False
        self.pon: bool = False
        self.kan: bool = False
        self.tsumo: bool = False
        self.ron: bool = False


class Player:
    _id_generator = None

    def __init__(self, socket_id: str, name: str, room_id: int):
        if Player._id_generator is None:
            Player._id_generator = self._generate_id()

        self._id = next(Player._id_generator)
        self.socket_id = socket_id
        self.name = name
        self.room_id = room_id
        self.ready: bool = False

        self.score: int = 0
        self.hand: Hand = Hand()
        self.seat_wind: str = ""
        self.discarded_tiles: List[Tile] = []
        self.is_riichi: bool = False
        self.selected_tiles = []
        self.voted: int = 0
        self.round_score = 1000

        self.action = Action()
        self.stop_ron = eventlet.event.Event()
        self.score_info = Score()

    def to_dict(self):
        discarded_tiles = [t.__dict__ for t in self.discarded_tiles]
        selected_tiles = [t.__dict__ for t in self.selected_tiles]
        return {
            "id": self.id,
            "socket_id": self.socket_id,
            "name": self.name,
            "room_id": self.room_id,
            "score": self.score,
            "hand": self.hand.to_dict(),
            "seat_wind": self.seat_wind,
            "discarded_tiles": discarded_tiles,
            "is_riichi": self.is_riichi,
            "score_info": self.score_info.__dict__,
            "selected_tiles": selected_tiles,
            "voted": self.voted,
            "round_score": self.round_score,
        }

    def initialize(self):
        self.score: int = 0
        self.hand: Hand = Hand()
        self.seat_wind: str = ""
        self.discarded_tiles: List[Tile] = []
        self.is_riichi: bool = False
        self.action = Action()
        self.score_info = Score()
        self.selected_tiles = []
        self.voted = 0
        self.round_score = 1000

    def next_round(self):
        self.hand: Hand = Hand()
        self.discarded_tiles: List[Tile] = []
        self.is_riichi: bool = False
        self.action = Action()
        seat_order = ["east", "south", "west", "north"]
        current_seat_index = seat_order.index(self.seat_wind)
        next_seat_index = (current_seat_index + 1) % len(seat_order)
        self.seat_wind = seat_order[next_seat_index]
        self.score_info = Score()
        self.selected_tiles = []
        self.voted = 0
        self.round_score = 1000

    @property
    def id(self):
        return self._id

    @staticmethod
    def _generate_id():
        player_id = 1
        while True:
            yield player_id
            player_id += 1

    def update_score(self, new_score: int):
        self.score = new_score

    def update_discrded_tiles(self, tile: Tile):
        self.discarded_tiles.append(tile)

    def update_seat_wind(self, new_wind: str):
        valid_winds = ["東", "南", "西", "北"]
        if new_wind in valid_winds:
            self.seat_wind = new_wind
        else:
            raise ValueError(
                "Invalid wind. Please provide one of: '東', '南', '西', '北'")

    def riichi(self):
        self.is_riichi = True

    def reset_riichi(self):
        self.is_riichi = False
