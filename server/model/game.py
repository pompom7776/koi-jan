from dataclasses import dataclass, field
from typing import List

from model.round import Round


@dataclass
class Game:
    id: int
    room_id: int
    rounds: List[Round] = field(default_factory=list)
