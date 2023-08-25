from dataclasses import dataclass, field
from typing import List

from model.tile import Tile


@dataclass
class Call:
    type: str
    tiles: List[Tile]
    target_player_id: int
    target_tile_id: int


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
