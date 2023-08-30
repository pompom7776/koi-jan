from dataclasses import dataclass
from typing import List

from model.tile import Tile


@dataclass
class Call:
    type: str
    tiles: List[Tile]
    target_player_id: int
    target_tile_id: int
