from model.game import Game
import repository.db.game as game_repo


def setup_game(room_id: int) -> Game:
    game = game_repo.create_game(room_id)

    return game
