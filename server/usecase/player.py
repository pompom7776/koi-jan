import repository.player
from model.player import Player


def register_player(player_name: str, socket_id: str) -> Player:
    player_id = repository.player.create_player(player_name, socket_id)
    player = repository.player.fetch_player(player_id)

    return player


def get_player_by_socket_id(socket_id: str) -> Player:
    player = repository.player.fetch_player_by_socket_id(socket_id)

    return player
