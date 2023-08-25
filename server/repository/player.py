from typing import List

from db.database import execute_query, fetch_data
from model.player import Player
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
        "WHERE d.round_id = %s AND d.player_id = %s "
        "AND NOT EXISTS ("
        "    SELECT 1 "
        "    FROM discard dc "
        "    WHERE dc.round_id = d.round_id "
        "    AND dc.player_id = d.player_id "
        "    AND dc.tile_id = d.tile_id"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 "
        "    FROM call c "
        "    WHERE c.round_id = d.round_id "
        "    AND c.call_player_id = d.player_id "
        "    AND c.targettile_id = d.tile_id"
        ") "
        "AND NOT EXISTS ("
        "    SELECT 1 "
        "    FROM agari a "
        "    WHERE a.round_id = d.round_id "
        "    AND a.player_id = d.player_id "
        "    AND a.type = 'ron'"
        ")"
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
