from dataclasses import dataclass


@dataclass
class Reaction:
    id: int
    name: str
    player_id: int
