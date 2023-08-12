class Tile:
    def __init__(self,
                 id: int = 0,
                 suit: str = "-",
                 rank: int = 0,
                 name: str = "-"):
        self.id = id
        self.suit = suit
        self.rank = rank
        self.name = name
        self.can_riichi = False
