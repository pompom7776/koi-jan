class Tile:
    def __init__(self, id: int = 0, suit: str = "", rank: int = 0,
                 name: str = "", bonus: bool = False):
        self.id = id
        self.suit = suit
        self.rank = rank
        self.name = name
        self.bonus = bonus

    # 例: id: 1, suit: souzu, rank: 1, name: 1s
    def __str__(self):
        return (f"id: {self.id}, "
                f"suit: {self.suit}, "
                f"rank: {self.rank}, "
                f"name: {self.name}, "
                f"bonus: {self.bonus}")
