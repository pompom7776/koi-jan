from typing import List, Tuple

from db.database import execute_query, fetch_data
from model.tile import Tile


def discard_tile(round_id: int, player_id: int, tile_id: int):
    query = (
        "INSERT INTO discard (round_id, player_id, tile_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (round_id, player_id, tile_id))


def fetch_discarded_tiles(round_id: int, player_id: int) -> List[Tile]:
    query = (
        "SELECT t.id, t.suit, t.rank, t.name "
        "FROM discard d "
        "JOIN tile t ON d.tile_id = t.id "
        "WHERE d.round_id = %s AND d.player_id = %s "
        "ORDER BY d.id ASC"
    )
    result = fetch_data(query, (round_id, player_id))

    discarded: List[Tile] = []
    for row in result:
        tile = Tile(id=row[0], suit=row[1], rank=row[2], name=row[3])
        discarded.append(tile)

    return discarded


def fetch_latest_discarded_tile(round_id: str) -> Tuple[int, int]:
    query = (
        "SELECT tile_id, player_id "
        "FROM discard "
        "WHERE round_id = %s "
        "ORDER BY discard_time DESC "
        "LIMIT 1"
    )
    result = fetch_data(query, (round_id,))

    if result:
        tile_id, player_id = result[0]
        return tile_id, player_id
    else:
        return None
