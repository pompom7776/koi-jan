import random
from tile import Tile


class Wall:
    def __init__(self):
        self.tiles = []
        self.dead_tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def initialize(self):
        self.tiles = []
        for suit in ["manzu", "pinzu", "souzu"]:
            for rank in range(1, 10):
                name = f"{rank}{suit[0]}"
                for i in range(4):
                    if rank == 5 and i == 0:
                        tile = Tile(len(self.tiles) + 1,
                                    suit, rank, name, True)
                    else:
                        tile = Tile(len(self.tiles) + 1, suit, rank, name)
                    self.add_tile(tile)
        suit = "wind"
        names = ["east", "south", "west", "north"]
        for i, name in enumerate(names):
            for _ in range(4):
                tile = Tile(len(self.tiles) + 1, suit, i+1, name)
                self.add_tile(tile)
        suit = "dragon"
        names = ["white", "green", "red"]
        for i, name in enumerate(names):
            for _ in range(4):
                tile = Tile(len(self.tiles) + 1, suit, i+1, name)
                self.add_tile(tile)

    def shuffle(self):
        random.shuffle(self.tiles)

    def draw_tile(self):
        if self.tiles:
            return self.tiles.pop()
        else:
            raise IndexError("The wall is empty.")

    def get_remaining(self):
        return len(self.tiles)
