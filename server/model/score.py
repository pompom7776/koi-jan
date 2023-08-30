from dataclasses import dataclass, field
from typing import List


@dataclass
class Score:
    id: int
    score: int
    han: int
    fu: int
    yaku: List[str] = field(default_factory=list)
