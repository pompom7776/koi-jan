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
