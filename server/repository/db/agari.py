from typing import List

from db.database import execute_query, fetch_data
from model.score import Score


def agari(round_id: int,
          player_id: int,
          target_player_id: str,
          target_tile_id: int,
          agari_type: str) -> int:
    query = (
        "INSERT INTO agari (round_id, player_id, "
        "target_player_id, target_tile_id, type) "
        "VALUES (%s, %s, %s, %s, %s) "
        "RETURNING id"
    )
    result = execute_query(query,
                           (round_id, player_id,
                            target_player_id, target_tile_id, agari_type),
                           ("id", ))

    if result:
        agari_id = result["id"]

        return agari_id
    else:
        return None


def set_score(agari_id: int,
              score: int,
              han: int,
              fu: int,
              yaku_en_names: List[str]) -> Score:
    query = (
        "INSERT INTO score (agari_id, score, han, fu) "
        "VALUES (%s, %s, %s, %s) "
        "RETURNING id, score, han, fu"
    )
    result = execute_query(query,
                           (agari_id, score, han, fu),
                           ("id", "score", "han", "fu"))
    score_id = result["id"]
    score_value = result["score"]
    han = result["han"]
    fu = result["fu"]
    score = Score(score_id, score_value, han, fu)

    query = (
        "INSERT INTO score_yaku (score_id, yaku_id) "
        "VALUES (%s, (SELECT id FROM yaku WHERE en_name = %s))"
    )
    for en_name in yaku_en_names:
        execute_query(query, (score_id, en_name))

    query = (
        "SELECT ja_name "
        "FROM yaku "
        "WHERE en_name IN %s"
    )
    result = fetch_data(query, (tuple(yaku_en_names),))
    score.yaku = [row[0] for row in result]

    return score


def fetch_score(round_id: int, player_id: int) -> Score:
    query = (
        "SELECT s.id, s.score, s.han, s.fu "
        "FROM score s "
        "JOIN agari a ON s.agari_id = a.id "
        "WHERE a.round_id = %s AND a.player_id = %s "
    )
    result = fetch_data(query, (round_id, player_id))

    if result:
        score_id = result[0][0]
        score_value = result[0][1]
        han = result[0][2]
        fu = result[0][3]
        score = Score(score_id, score_value, han, fu)
    else:
        return None

    query = (
        "SELECT y.ja_name "
        "FROM yaku y "
        "JOIN score_yaku sy ON y.id = sy.yaku_id "
        "WHERE sy.score_id = %s"
    )
    result = fetch_data(query, (score_id,))

    if result:
        for row in result:
            score.yaku.append(row[0])
    return score


def fetch_agari(round_id: int, player_id: int) -> bool:
    query = (
        "SELECT 1 "
        "FROM agari "
        "WHERE round_id = %s AND player_id = %s"
    )
    result = fetch_data(query, (round_id, player_id))

    if result:
        return True
    else:
        return False


def fetch_agari_count(round_id: int) -> int:
    query = (
        "SELECT COUNT(*) "
        "FROM agari "
        "WHERE round_id = %s"
    )
    result = fetch_data(query, (round_id,))

    if result:
        return result[0][0]
    else:
        return None
