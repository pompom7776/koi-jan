from model.game import Game
import repository.db.game as game_repo


def get_game_by_room_id(room_id: int) -> Game:
    game = game_repo.fetch_game(room_id)

    return game
