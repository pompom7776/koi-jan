from typing import List

from db.database import execute_query
from model.tile import Tile
from model.wall import Wall, MAX_TILE_NUMBER


def create_wall(tiles: List[Tile]) -> Wall:
    query = (
        "INSERT INTO wall (remaining_number, dora_number) "
        "VALUES (%s, %s) RETURNING id, remaining_number, dora_number"
    )
    result = execute_query(query,
                           (MAX_TILE_NUMBER, 1),
                           ("id", "remaining_number", "dora_number"))

    if result:
        wall_id = result["id"]
        remaining_number = result["remaining_number"]
        dora_number = result["dora_number"]

        for tile in tiles:
            query = (
                "INSERT INTO wall_tile (wall_id, tile_id) "
                "VALUES (%s, %s)"
            )
            execute_query(query, (wall_id, tile.id))

        wall = Wall(wall_id, remaining_number, dora_number, tiles)
        return wall
    else:
        return None
