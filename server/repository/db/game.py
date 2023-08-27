from db.database import execute_query, fetch_data
from model.game import Game


def create_game(room_id: int) -> Game:
    query = (
        "INSERT INTO game (room_id, end_time) "
        "VALUES (%s, %s) RETURNING id, room_id, start_time, end_time"
    )
    result = execute_query(query,
                           (room_id, None),
                           ("id", "room_id", "start_time", "end_time"))

    if result:
        id = result["id"]
        room_id = result["room_id"]
        game = Game(id, room_id)
        return game
    else:
        return None


def fetch_game(room_id: int) -> Game:
    query = (
        "SELECT id, room_id "
        "FROM game "
        "WHERE room_id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (room_id,))

    if result:
        id, room_id = result[0]
        return Game(id, room_id)
    else:
        return None
