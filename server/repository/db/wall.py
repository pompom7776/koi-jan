from typing import List

from db.database import execute_query, fetch_data
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

        wall = Wall(wall_id, remaining_number-14, dora_number, tiles)
        return wall
    else:
        return None


def fetch_wall(wall_id: int) -> Wall:
    query = (
        "SELECT * "
        "FROM wall "
        "WHERE id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (wall_id,))

    if result:
        id, remaining_number, dora_number = result[0]
        return Wall(id, remaining_number-14, dora_number, [])
    else:
        return None


def fetch_dora(wall_id: int) -> List[Tile]:
    query = (
        "SELECT dora_number "
        "FROM wall "
        "WHERE id = %s"
    )
    dora_number = fetch_data(query, (wall_id, ))[0][0]

    query = (
        "SELECT t.id, t.suit, t.rank, t.name "
        "FROM tile t "
        "JOIN wall_tile wt ON t.id = wt.tile_id "
        "WHERE wt.wall_id = %s "
        "ORDER BY wt.id DESC "
        "LIMIT %s"
    )
    result = fetch_data(query, (wall_id, dora_number))[0]

    dora_tiles = []
    dora_tiles.append(Tile(id=result[0],
                           suit=result[1],
                           rank=result[2],
                           name=result[3]))

    return dora_tiles


def fetch_remaining_number(wall_id: int) -> int:
    query = (
        "SELECT remaining_number "
        "FROM wall "
        "WHERE id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (wall_id,))

    if result:
        remaining_number = result[0][0]
        return remaining_number - 14
    else:
        return None
