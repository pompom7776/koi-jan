from dataclasses import dataclass, field
from typing import List

from model.call import Call
from model.tile import Tile
from model.score import Score


@dataclass
class Player:
    id: int
    name: str
    socket_id: str
    hand: List[Tile] = field(default_factory=list)
    tsumo: Tile = None
    discarded: List[Tile] = field(default_factory=list)
    call: List[Call] = field(default_factory=list)
    is_riichi: bool = False
    agari: bool = False
    score: Score = None
    selected: List[Tile] = field(default_factory=list)
