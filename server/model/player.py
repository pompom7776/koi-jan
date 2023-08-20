from dataclasses import dataclass


@dataclass
class Player:
    id: int
    socket_id: str
    name: str
