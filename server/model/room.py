from typing import List

import eventlet

from model.table import Table
from model.player import Player
from model.hand import TileFromPlayer


class Flag:
    def __init__(self):
        self.tsumo = True
        self.agari_num = 0


class Waiter:
    def __init__(self):
        self.pon: Player = None
        self.kan: Player = None
        self.ron: List[Player] = []


class RoomWaitEvent:
    def __init__(self):
        self.tsumo = eventlet.event.Event()
        self.vote = eventlet.event.Event()


class Room:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.players = []
        self.skip_players: List[Player] = []
        self.table: Table = Table()
        self.current_player: id = 0
        self.votes: int = 0
        self.flag: Flag = Flag()
        self.waiter: Waiter = Waiter()
        self.wait_event: RoomWaitEvent = RoomWaitEvent()
        self.tmp_tiles: TileFromPlayer = TileFromPlayer()
