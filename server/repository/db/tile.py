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


def fetch_tile(tile_id: int) -> Tile:
    query = (
        "SELECT * FROM tile "
        "WHERE id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (tile_id,))

    if result:
        id, suit, rank, name = result[0]
        tile = Tile(id, suit, rank, name)
        return tile
    else:
        return None
