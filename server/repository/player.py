from typing import List

from db.database import execute_query, fetch_data
from model.player import Player, Call
from model.tile import Tile


def create_player(name: str, socket_id: str) -> int:
    query = (
        "INSERT INTO player "
        "DEFAULT VALUES RETURNING id"
    )
    result = execute_query(query, None, ("id", ))
    player_id = result["id"]

    query = (
        "INSERT INTO player_detail (player_id, name, socket_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (player_id, name, socket_id))

    return player_id


def fetch_player(player_id: int) -> Player:
    query = (
        "SELECT pd.player_id, pd.name, pd.socket_id "
        "FROM player_detail pd "
        "WHERE pd.player_id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (player_id,))

    if result:
        player_id, name, socket_id = result[0]
        return Player(player_id, name, socket_id)
    else:
        return None


def fetch_player_by_socket_id(socket_id: str) -> Player:
    query = (
        "SELECT pd.player_id, pd.name, pd.socket_id "
        "FROM player_detail pd "
        "WHERE pd.socket_id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (socket_id,))

    if result:
        player_id, name, socket_id = result[0]
        return Player(player_id, name, socket_id)
    else:
        return None


def update_player_socket_id(new_socket_id: str, old_socket_id: str):
    query = (
        "UPDATE player_detail "
        "SET socket_id = %s "
        "WHERE socket_id = %s"
    )
    execute_query(query, (new_socket_id, old_socket_id))


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


def fetch_hand(round_id: int, player_id: int) -> List[Tile]:
    query = (
        "SELECT d.tile_id "
        "FROM draw d "
        "LEFT JOIN ( "
        "  SELECT dc.round_id, dc.player_id, dc.tile_id "
        "  FROM discard dc "
        "  UNION "
        "  SELECT a.round_id, a.player_id, a.target_tile_id AS tile_id "
        "  FROM agari a "
        "  WHERE a.type = 'ron' "
        "  UNION "
        "  SELECT c.round_id, c.call_player_id AS player_id, ct.tile_id "
        "  FROM call c "
        "  JOIN call_tile ct ON c.id = ct.call_id "
        ") "
        "used_tiles ON d.round_id = used_tiles.round_id "
        "  AND d.player_id = used_tiles.player_id "
        "  AND d.tile_id = used_tiles.tile_id "
        "WHERE d.round_id=%s AND d.player_id=%s "
        "  AND used_tiles.round_id IS NULL"
    )
    tile_ids = fetch_data(query, (round_id, player_id))

    if tile_ids:
        query = (
            "SELECT t.id, t.suit, t.rank, t.name "
            "FROM tile t "
            "WHERE t.id IN %s"
        )
        tiles_data = fetch_data(query, (tuple(tile[0] for tile in tile_ids),))

        hand_tiles = [Tile(id=row[0], suit=row[1], rank=row[2], name=row[3])
                      for row in tiles_data]
        return hand_tiles
    else:
        return []


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
    print(result)
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
