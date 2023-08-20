from db.database import execute_query, fetch_data
from model.player import Player


def create_player(name: str, socket_id: str) -> int:
    query = (
        "INSERT INTO player "
        "VALUES () RETURNING id"
    )
    player_id = execute_query(query, (), ("id", ))

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


def update_player_socket_id(old_socket_id: str, new_socket_id: str) -> Player:
    query = (
        "UPDATE player_detail "
        "SET socket_id = %s "
        "WHERE socket_id = %s"
    )
    execute_query(query, (new_socket_id, old_socket_id))
