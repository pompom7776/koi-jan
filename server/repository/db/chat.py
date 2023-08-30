from typing import List

from db.database import execute_query, fetch_data
from model.chat import Chat


def send_message(room_id: int,
                 player_id: int,
                 message: str):
    query = (
        "INSERT INTO send_chat (room_id, player_id, message) "
        "VALUES (%s, %s, %s)"
    )
    execute_query(query, (room_id, player_id, message))


def fetch_chats(room_id: int) -> List[Chat]:
    query = (
        "SELECT id, player_id, message "
        "FROM send_chat "
        "WHERE room_id = %s "
        "LIMIT 50"
    )
    result = fetch_data(query, (room_id,))

    chats = []
    for row in result:
        chat_id, player_id, message = row
        query = (
            "SELECT name "
            "FROM player_detail "
            "WHERE id = %s"
        )
        player_name = fetch_data(query, (player_id,))[0][0]

        chat = Chat(chat_id, player_id, player_name, message)
        chats.append(chat)

    return chats
