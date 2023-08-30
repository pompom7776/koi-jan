from typing import List, Tuple

from db.database import execute_query, fetch_data
from model.tile import Tile
from model.wall import MAX_TILE_NUMBER


def draw_tile(round_id: int,
              player_id: int,
              draw_number: int = 1) -> List[Tile]:
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

    if remaining_number <= 80:
        return None

    query = (
        "SELECT t.id, t.suit, t.rank, t.name "
        "FROM tile t "
        "JOIN wall_tile wt ON t.id = wt.tile_id "
        "WHERE wt.wall_id = %s "
        "ORDER BY wt.id "
        "LIMIT %s OFFSET %s"
    )
    drawn_tile_count = MAX_TILE_NUMBER - remaining_number
    result = fetch_data(query, (wall_id, draw_number, drawn_tile_count))

    tiles = []
    for row in result:
        tile = Tile(id=row[0], suit=row[1], rank=row[2], name=row[3])
        tiles.append(tile)

    remaining_number -= draw_number
    query = (
        "UPDATE wall "
        "SET remaining_number = %s "
        "WHERE id = %s"
    )
    execute_query(query, (remaining_number, wall_id))

    for tile in tiles:
        query = (
            "INSERT INTO draw (round_id, player_id, tile_id) "
            "VALUES (%s, %s, %s)"
        )
        execute_query(query, (round_id, player_id, tile.id))

    return tiles


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


def fetch_latest_draw_tile(round_id: str) -> Tuple[int, int]:
    query = (
        "SELECT tile_id, player_id "
        "FROM draw "
        "WHERE round_id = %s "
        "ORDER BY draw_time DESC "
        "LIMIT 1"
    )
    result = fetch_data(query, (round_id,))

    if result:
        tile_id, player_id = result[0]
        return tile_id, player_id
    else:
        return None, None
