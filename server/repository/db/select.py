from typing import List

from db.database import execute_query, fetch_data
from model.tile import Tile


def select_tile(round_id: int, player_id: int, tile_id: int):
    query = (
        "INSERT INTO select_tile (round_id, player_id, tile_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (round_id, player_id, tile_id))


def delete_tile(round_id: int, player_id: int, tile_id: int):
    query = (
        "DELETE FROM select_tile "
        "WHERE round_id = %s AND player_id = %s AND tile_id = %s"
    )
    execute_query(query, (round_id, player_id, tile_id))


def fetch_select_tiles(round_id: int, player_id: int) -> List[Tile]:
    query = (
        "SELECT tile_id "
        "FROM select_tile "
        "WHERE round_id = %s AND player_id = %s"
    )
    result = fetch_data(query, (round_id, player_id))

    tiles = []
    if result:
        select_tile_ids = [row[0] for row in result]
        for tile_id in select_tile_ids:
            query = (
                "SELECT * FROM tile "
                "WHERE id = %s "
                "LIMIT 1"
            )
            tile_result = fetch_data(query, (tile_id,))

            if tile_result:
                id, suit, rank, name = tile_result[0]
                tile = Tile(id, suit, rank, name)
                tiles.append(tile)

    return tiles
