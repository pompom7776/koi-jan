from dataclasses import dataclass, field
from typing import List

from model.tile import Tile


@dataclass
class Player:
    id: int
    name: str
    socket_id: str
    hand: List[Tile] = field(default_factory=list)
    tsumo: Tile = None
    discarded: List[Tile] = field(default_factory=list)
