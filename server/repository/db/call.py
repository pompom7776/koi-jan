from typing import List

from db.database import execute_query, fetch_data
from model.call import Call
from model.tile import Tile


def call(round_id: int,
         call_type: str,
         caller_id: int,
         target_player_id: int,
         target_tile_id: int) -> int:
    query = (
        "INSERT INTO call (round_id, type, "
        "call_player_id, target_player_id, target_tile_id) "
        "VALUES (%s, %s, %s, %s, %s) "
        "RETURNING id"
    )
    result = execute_query(query,
                           (round_id, call_type, caller_id,
                            target_player_id, target_tile_id),
                           ("id", ))
    if result:
        call_id = result["id"]
        return call_id
    else:
        return None


def call_tile(call_id: int, tile_id: int) -> int:
    query = (
        "INSERT INTO call_tile (call_id, tile_id) "
        "VALUES (%s, %s) "
    )
    execute_query(query, (call_id, tile_id))


def fetch_call(round_id: int, player_id: int) -> List[Call]:
    query = (
        "SELECT id, type, target_player_id, target_tile_id "
        "FROM call "
        "WHERE round_id = %s AND call_player_id = %s"
    )
    result = fetch_data(query, (round_id, player_id))
    calls = []
    for call_id, call_type, target_player_id, target_tile_id in result:
        query = (
            "SELECT tile_id "
            "FROM call_tile "
            "WHERE call_id = %s"
        )
        tile_ids = [record[0] for record in fetch_data(query, (call_id,))]

        tiles = []
        for tile_id in tile_ids:
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

        call = Call(type=call_type,
                    tiles=tiles,
                    target_player_id=target_player_id,
                    target_tile_id=target_tile_id)
        calls.append(call)

    return calls
