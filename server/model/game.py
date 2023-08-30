from dataclasses import dataclass

from model.round import Round


@dataclass
class Game:
    id: int
    room_id: int
    # 送信量が多くなるため、roundは最新のを一つ所持するだけにする
    # rounds: List[Round] = field(default_factory=list)
    round: Round = None
