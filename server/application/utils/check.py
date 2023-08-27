from model.player import Player
from model.tile import Tile
from application.utils.score import agari


def pon(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 2 and not player.is_riichi:
        return True

    return False


def kan(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 3 and not player.is_riichi:
        return True

    return False


def ron(player: Player, tile: Tile, seat_wind: str, round_wind: str):
    player.hand.append(tile)
    result = agari(player, tile, [], seat_wind, round_wind)
    player.hand.pop(-1)
    if result.yaku is not None:
        return True
    return False
