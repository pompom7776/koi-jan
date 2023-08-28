from dataclasses import dataclass


@dataclass
class Tile:
    id: int
    suit: str
    rank: int
    name: str
    riichi: bool = False
    can_riichi: bool = False
