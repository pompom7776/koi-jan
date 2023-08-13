from typing import List

import eventlet

from model.tile import Tile
from model.hand import Hand
from model.score import Score


class Action:
    def __init__(self):
        self.riichi: bool = False
        self.chi: bool = False
        self.pon: bool = False
        self.kan: bool = False
        self.tsumo: bool = False
        self.ron: bool = False


class PlayerWaitEvent:
    def __init__(self):
        self.ron = eventlet.event.Event()


class Player:
    _id_generator = None

    def __init__(self,
                 socket_id: str,
                 name: str,
                 room_id: int):
        if Player._id_generator is None:
            Player._id_generator = self._generate_id()

        self._id: int = next(Player._id_generator)
        self.socket_id = socket_id
        self.name = name
        self.room_id = room_id

        self.ready: bool = False
        self.is_riichi: bool = False
        self.score: int = 0
        self.score_info: Score = Score()
        self.round_score = 1000
        self.seat_wind: str = ""
        self.hand: Hand = Hand()
        self.discarded_tiles: List[Tile] = []
        self.selected_tiles: List[Tile] = []
        self.voted: int = 0
        self.action: Action = Action()
        self.wait_event: PlayerWaitEvent = PlayerWaitEvent()

    @property
    def id(self):
        return self._id

    @staticmethod
    def _generate_id():
        player_id = 1
        while True:
            yield player_id
            player_id += 1
