from dataclasses import dataclass, field
from typing import List

from model.tile import Tile


@dataclass
class Tiles:
    player_id: int
    tiles: List[Tile] = field(default_factory=list)
