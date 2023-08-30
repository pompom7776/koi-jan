from typing import List

from db.database import execute_query, fetch_data
from model.reaction import Reaction


def send_reaction(room_id: int,
                  player_id: int,
                  reaction_id: int):
    query = (
        "INSERT INTO send_reaction (room_id, player_id, reaction_id) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (room_id, player_id, reaction_id))


def fetch_reaction(reaction_id: int) -> Reaction:
    query = (
        "SELECT id, name "
        "FROM reaction "
        "WHERE id = %s"
    )
    result = fetch_data(query, (reaction_id,))

    if result:
        reaction = Reaction(result[0][0], result[0][1])
        return reaction
    else:
        return None
