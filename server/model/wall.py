from dataclasses import dataclass
from typing import List

from model.tile import Tile


MAX_TILE_NUMBER = 136


@dataclass
class Wall:
    id: int
    remaining_number: int
    dora_number: int
    tiles: List[Tile]
