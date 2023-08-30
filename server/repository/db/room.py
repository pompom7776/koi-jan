from typing import List

from db.database import execute_query, fetch_data
from model.player import Player
from model.room import Room


def create_room(room_number: int, player_id: int) -> Room:
    query = (
        "INSERT INTO room (room_number) "
        "VALUES (%s) RETURNING id"
    )
    result = execute_query(query, (room_number, ), ("id", ))
    room_id = result["id"]

    query = (
        "INSERT INTO create_room (room_id, host_id) "
        "VALUES (%s, %s)"
    )
    execute_query(query, (room_id, player_id))

    return Room(room_id, room_number)


def close_room(room_id: int):
    query = (
        "INSERT INTO close_room (room_id) "
        "VALUES (%s)"
    )
    execute_query(query, (room_id, ))


def enter_room(room_id: int, player_id: int):
    query = (
        "INSERT INTO enter_room (room_id, player_id) "
        "VALUES (%s, %s)"
    )
    execute_query(query, (room_id, player_id))


def leave_room(room_id: int, player_id: int):
    query = (
        "INSERT INTO leave_room (room_id, player_id) "
        "VALUES (%s, %s)"
    )
    execute_query(query, (room_id, player_id))


def ready_room(room_id: int, player_id: int):
    query = (
        "INSERT INTO ready_room (room_id, player_id) "
        "VALUES (%s, %s)"
    )
    execute_query(query, (room_id, player_id))


def unready_room(room_id: int, player_id: int):
    query = (
        "SELECT id FROM ready_room "
        "WHERE room_id = %s AND player_id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (room_id, player_id))
    if result:
        ready_room_id = result[0]
    else:
        ready_room_id = None

    query = (
        "DELETE FROM ready_room "
        "WHERE id = %s"
    )
    execute_query(query, (ready_room_id, ))


def fetch_room(room_id: int) -> Room:
    query = (
        "SELECT * FROM room "
        "WHERE id = %s "
        "LIMIT 1"
    )
    result = fetch_data(query, (room_id,))

    if result:
        id, room_number = result[0]
        return Room(id, room_number)
    else:
        return None


def fetch_open_rooms() -> List[Room]:
    query = (
        "SELECT r.id, r.room_number "
        "FROM room r "
        "LEFT JOIN create_room cr ON r.id = cr.room_id "
        "LEFT JOIN close_room cl ON r.id = cl.room_id "
        "WHERE cr.id IS NOT NULL AND cl.id IS NULL"
    )
    result = fetch_data(query)

    open_rooms = []
    for row in result:
        room_id, room_number = row
        open_rooms.append(Room(room_id, room_number))

    return open_rooms


def fetch_open_room_by_player_id(player_id: int) -> Room:
    query = (
        "SELECT r.id, r.room_number "
        "FROM room r "
        "INNER JOIN create_room cr ON r.id = cr.room_id "
        "LEFT JOIN close_room cl ON r.id = cl.room_id "
        "INNER JOIN enter_room er ON r.id = er.room_id "
        "WHERE cr.id IS NOT NULL AND cl.id IS NULL "
        "AND er.player_id = %s"
    )
    result = fetch_data(query, (player_id,))

    if result:
        room_id, room_number = result[0]
        room = Room(room_id, room_number)
        return room
    else:
        return None


def fetch_players_in_room(room_id: int) -> List[Player]:
    query = (
        "SELECT pd.player_id, pd.name, pd.socket_id "
        "FROM player_detail pd "
        "INNER JOIN enter_room er ON pd.player_id = er.player_id "
        "WHERE er.room_id = %s"
    )
    result = fetch_data(query, (room_id,))

    players = []
    for row in result:
        player_id, name, socket_id = row
        player = Player(player_id, name, socket_id)
        players.append(player)

    return players
