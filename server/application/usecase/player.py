import repository.db.player as player_repo
from model.player import Player


def register_player(player_name: str, socket_id: str) -> Player:
    player_id = player_repo.create_player(player_name, socket_id)
    player = player_repo.fetch_player(player_id)

    return player


def get_player_by_socket_id(socket_id: str) -> Player:
    player = player_repo.fetch_player_by_socket_id(socket_id)

    return player
