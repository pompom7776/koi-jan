from dataclasses import dataclass


@dataclass
class Chat:
    id: int
    player_id: int
    player_name: str
    message: str
