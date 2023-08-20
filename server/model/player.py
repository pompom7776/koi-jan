from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    socket_id: str
