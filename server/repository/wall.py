from typing import List

from db.database import execute_query, fetch_data
from model.tile import Tile
from model.wall import MAX_TILE_NUMBER


def create_wall(tiles: List[Tile]) -> int:
    query = (
        "INSERT INTO wall (remaining_number, dora_number) "
        "VALUES (%s, %s) RETURNING id"
    )
    result = execute_query(query,
                           (MAX_TILE_NUMBER, 1),
                           ("id", ))

    if result:
        wall_id = result["id"]

        for tile in tiles:
            query = (
                "INSERT INTO wall_tile (wall_id, tile_id) "
                "VALUES (%s, %s)"
            )
            execute_query(query, (wall_id, tile.id))

        return wall_id
    else:
        return None


def draw_tile(round_id: int, player_id: int) -> Tile:
    query = (
        "SELECT wall_id "
        "FROM round "
        "WHERE id = %s"
    )
    wall_id = fetch_data(query, (round_id, ))[0][0]

    query = (
        "SELECT remaining_number "
        "FROM wall "
        "WHERE id = %s"
    )
    remaining_number = fetch_data(query, (wall_id, ))[0][0]

    if remaining_number <= 14:
        return None

    query = (
        "SELECT t.id, t.suit, t.rank, t.name "
        "FROM tile t "
        "JOIN wall_tile wt ON t.id = wt.tile_id "
        "WHERE wt.wall_id = %s "
        "ORDER BY wt.id "
        "LIMIT 1 OFFSET %s"
    )
    drawn_tile_count = MAX_TILE_NUMBER - remaining_number
    result = fetch_data(query, (wall_id, drawn_tile_count))[0]

    tile = Tile(id=result[0], suit=result[1], rank=result[2], name=result[3])

    remaining_number -= 1
    query = (
        "UPDATE wall "
        "SET remaining_number = %s "
        "WHERE id = %s"
    )
    execute_query(query, (remaining_number, wall_id))

    return tile


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
