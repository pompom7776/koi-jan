from db.database import execute_query, fetch_data


def vote(round_id: int, vote_player_id: int, target_player_id: int):
    query = (
        "INSERT INTO vote (round_id, vote_player_id, target_player_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (round_id, vote_player_id, target_player_id))


def fetch_vote_count(round_id: int) -> int:
    query = (
        "SELECT COUNT(*) "
        "FROM vote "
        "WHERE round_id = %s"
    )
    result = fetch_data(query, (round_id,))

    if result:
        return result[0][0]
    else:
        return None
