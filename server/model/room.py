from typing import List

from model.table import Table
from model.player import Player


class Flag:
    def __init__(self):
        self.tsumo = True
        self.agari_num = 0


class Room:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.players = []
        self.skip_players: List[Player] = []
        self.table: Table = Table()
        self.turn: id = 0
        self.current_player: id = 0
        self.votes: int = 0
        self.flag: Flag = Flag()
