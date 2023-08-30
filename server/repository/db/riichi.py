from db.database import execute_query, fetch_data


def riichi(round_id: int, player_id: int, tile_id: int):
    query = (
        "INSERT INTO riichi (round_id, player_id, tile_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (round_id, player_id, tile_id))


def fetch_riichi(round_id: int, player_id: int) -> bool:
    query = (
        "SELECT 1 "
        "FROM riichi "
        "WHERE round_id = %s AND player_id = %s"
    )
    result = fetch_data(query, (round_id, player_id))

    if result:
        print(player_id, True)
        return True
    else:
        print(player_id, False)
        return False
