from model.round import Round, WINDS
import repository.db.round as round_repo
import repository.db.wall as wall_repo


def get_round(round_id: int) -> Round:
    round = round_repo.fetch_round(round_id)
    wall = wall_repo.fetch_wall(round.wall_id)
    round.wall_remaining_number = wall.remaining_number
    round.seat_winds = None
    round.dora = wall_repo.fetch_dora(wall.id)
    round.current_player_id = None

    return round


def get_round_id_by_room_id(room_id: int) -> int:
    round_id = round_repo.fetch_round_id_by_room_id(room_id)
    return round_id


def get_next_wind(current_wind):
    wind_index = WINDS.index(current_wind)
    if wind_index == len(WINDS) - 1:
        next_wind = WINDS[0]
    else:
        next_wind = WINDS[wind_index + 1]

    return next_wind
