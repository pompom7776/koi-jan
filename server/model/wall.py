from typing import List

from model.tile import Tile


class Wall:
    def __init__(self):
        self.tiles: List[Tile] = []
        self.dora_num: int = 1
        self.dora: List[Tile] = []
        self.ura_dora: List[Tile] = []
        # 嶺上牌
        self.dead_tiles: List[Tile] = []
