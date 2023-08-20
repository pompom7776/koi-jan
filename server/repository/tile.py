from typing import List

from db.database import fetch_data
from model.tile import Tile


def fetch_all_tiles() -> List[Tile]:
    query = (
        "SELECT * "
        "FROM tile"
    )
    result = fetch_data(query)

    tiles = []
    for row in result:
        id, suit, rank, name = row
        tile = Tile(id, suit, rank, name)
        tiles.append(tile)

    return tiles
