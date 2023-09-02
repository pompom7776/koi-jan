from db.database import execute_query, fetch_data
from model.round import Round, SeatWind


def create_round(game_id: int,
                 round_number: int,
                 round_wind: str,
                 dealer_id: int,
                 wall_id: int) -> Round:
    query = (
        "INSERT INTO round (game_id, round_number, round_wind, dealer_id, "
        "wall_id, end_time) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "RETURNING id, game_id, round_number, round_wind, dealer_id"
    )
    result = execute_query(query,
                           (game_id, round_number, round_wind, dealer_id,
                            wall_id, None),
                           ("id", "game_id", "round_number", "round_wind",
                            "dealer_id"))

    if result:
        id = result["id"]
        game_id = result["game_id"]
        round_number = result["round_number"]
        round_wind = result["round_wind"]
        dealer_id = result["dealer_id"]

        round = Round(id, game_id, round_number,
                      round_wind, dealer_id, wall_id)
        return round
    else:
        return None


def set_seat_wind(round_id: int,
                  player_id: int,
                  wind: str) -> SeatWind:
    query = (
        "INSERT INTO seat_wind (round_id, player_id, wind) "
        "VALUES (%s, %s, %s) "
        "RETURNING id, round_id, player_id, wind "
    )
    result = execute_query(query,
                           (round_id, player_id, wind),
                           ("id", "round_id", "player_id", "wind"))

    if result:
        id = result["id"]
        round_id = result["round_id"]
        player_id = result["player_id"]
        wind = result["wind"]

        seat_wind = SeatWind(id, round_id, player_id, wind)
        return seat_wind
    else:
        return None


def fetch_wind_by_player_id(round_id: int, player_id: int) -> str:
    query = (
        "SELECT sw.wind "
        "FROM seat_wind sw "
        "WHERE sw.round_id = %s AND sw.player_id = %s"
    )
    result = fetch_data(query, (round_id, player_id))

    if result:
        wind = result[0][0]
        return wind
    else:
        return None


def fetch_player_id_by_wind(round_id: int, wind: str) -> int:
    query = (
        "SELECT sw.player_id "
        "FROM seat_wind sw "
        "WHERE sw.round_id = %s AND sw.wind = %s"
    )
    result = fetch_data(query, (round_id, wind))

    if result:
        player_id = result[0][0]
        return player_id
    else:
        return None


def fetch_round_count(game_id: int) -> int:
    query = (
        "SELECT COUNT(*) "
        "FROM round "
        "WHERE game_id = %s"
    )
    result = fetch_data(query, (game_id,))

    if result:
        return result[0][0]
    else:
        return None


def fetch_round(round_id: int) -> Round:
    query = (
        "SELECT id, game_id, round_number, round_wind, dealer_id, wall_id "
        "FROM round "
        "WHERE id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (round_id,))

    if result:
        id, game_id, round_number, round_wind, dealer_id, wall_id = result[0]
        round = Round(id, game_id, round_number,
                      round_wind, dealer_id, wall_id)
        return round
    else:
        return None


def fetch_previous_round_id(game_id: int) -> int:
    query = (
        "SELECT id "
        "FROM round "
        "WHERE game_id = %s "
        "ORDER BY start_time DESC "
        "LIMIT 2"
    )

    result = fetch_data(query, (game_id,))

    if len(result) >= 2:
        return result[1][0]
    else:
        return None


def fetch_round_id_by_room_id(room_id: int) -> int:
    query = (
        "SELECT id "
        "FROM round "
        "WHERE game_id = (SELECT id FROM game WHERE room_id = %s) "
        "ORDER BY id DESC "
        "LIMIT 1"
    )
    result = fetch_data(query, (room_id, ))

    if result:
        round_id = result[0][0]
        return round_id
    else:
        return None


def fetch_current_player_id(round_id: int) -> int:
    query = (
        "SELECT player_id "
        "FROM ("
        "   SELECT call_player_id AS player_id, MAX(call_time) AS action_time "
        "   FROM call "
        "   WHERE round_id = %s "
        "   GROUP BY call_player_id "
        "   UNION ALL "
        "   SELECT player_id, MAX(draw_time) AS action_time "
        "   FROM draw "
        "   WHERE round_id = %s "
        "   GROUP BY player_id "
        "   UNION ALL "
        "   SELECT player_id, MAX(discard_time) AS action_time "
        "   FROM discard "
        "   WHERE round_id = %s "
        "   GROUP BY player_id "
        "   UNION ALL "
        "   SELECT player_id, MAX(agari_time) AS action_time "
        "   FROM agari "
        "   WHERE round_id = %s "
        "   GROUP BY player_id "
        ") AS all_actions "
        "ORDER BY action_time DESC "
        "LIMIT 1"
    )

    result = fetch_data(query, (round_id, round_id, round_id, round_id))

    if result:
        return result[0][0]
    else:
        return None
