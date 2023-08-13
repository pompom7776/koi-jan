import usecase.score
from model.tile import Tile
from model.hand import Hand
from model.player import Player, Action, PlayerWaitEvent
from model.score import Score


def initialize(player: Player):
    player.is_riichi = False
    player.score = 0
    player.round_score = 1000
    player.score_info = Score()
    player.hand = Hand()
    player.seat_wind = ""
    player.discarded_tiles = []
    player.selected_tiles = []
    player.voted = 0
    player.action = Action()
    player.wait_event = PlayerWaitEvent()


def can_pon(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand.tiles
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 2 and not player.is_riichi:
        return True

    return False


def can_kan(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand.tiles
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 3 and not player.is_riichi:
        return True

    return False


def can_ron(player: Player, tile: Tile, round_wind: str):
    player.hand.tiles.append(tile)
    agari = usecase.score.agari(player.hand,
                                tile,
                                [],
                                round_wind,
                                player.seat_wind,
                                False,
                                player.is_riichi)
    _ = player.hand.tiles.pop(-1)
    if agari.__dict__["yaku"] != []:
        return True

    return False
