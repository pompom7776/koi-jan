import repository.db.player as player_repo
from model.player import Player


def register_player(player_name: str, socket_id: str) -> Player:
    # if player_name == "":
    #     message: str = "名前を入力してください"
    #     emit.notify_error(socket_io, [socket_id], message)
    #     return
    player_id = player_repo.create_player(player_name, socket_id)
    player = player_repo.fetch_player(player_id)

    return player
