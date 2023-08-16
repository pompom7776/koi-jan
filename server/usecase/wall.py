import random

from model.tile import Tile
from model.wall import Wall


def initialize(wall: Wall):
    wall.tiles = []
    for suit in ["manzu", "pinzu", "souzu"]:
        for rank in range(1, 10):
            name = f"{rank}{suit[0]}"
            for _ in range(4):
                wall.tiles.append(Tile(len(wall.tiles) + 1, suit, rank, name))
    wind_names = ["east", "south", "west", "north"]
    for i, name in enumerate(wind_names):
        for _ in range(4):
            wall.tiles.append(Tile(len(wall.tiles) + 1, "wind", i+1, name))
    dragon_names = ["white", "green", "red"]
    for i, name in enumerate(dragon_names):
        for _ in range(4):
            wall.tiles.append(Tile(len(wall.tiles) + 1, "dragon", i+1, name))


def shuffle(wall: Wall):
    random.shuffle(wall.tiles)


def set_dead_tiles(wall: Wall):
    wall.dora_num = 1
    wall.dora = []
    wall.ura_dora = []
    wall.dead_tiles = []
    for _ in range(5):
        wall.dora.append(draw_tile(wall))
    for _ in range(5):
        wall.ura_dora.append(draw_tile(wall))
    for _ in range(4):
        wall.dead_tiles.append(draw_tile(wall))


def draw_tile(wall: Wall) -> Tile:
    return wall.tiles.pop()


def draw_dead_tile(wall: Wall) -> Tile:
    return wall.dead_tiles.pop()
