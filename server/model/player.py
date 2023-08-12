from typing import List

from model.tile import Tile
from model.hand import Hand


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

    def __init__(self,
                 socket_id: str,
                 name: str,
                 room_id: int):
        self._id: int = next(Player._id_generator)
        self.socket_id = socket_id
        self.name = name
        self.room_id = room_id

        self.ready: bool = False
        self.is_riichi: bool = False
        self.score: int = 0
        self.round_score = 1000
        self.seat_wind: str = ""
        self.hand: Hand = Hand()
        self.discarded_tiles: List[Tile] = []
        self.selected_tiles: List[Tile] = []
        self.voted: int = 0
        self.action = Action()
