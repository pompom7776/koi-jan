from dataclasses import dataclass, field
from typing import List

from model.player import Player
from model.game import Game


@dataclass
class Room:
    id: int
    number: int
    players: List[Player] = field(default_factory=list)
    game: Game = None
