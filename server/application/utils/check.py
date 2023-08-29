from model.player import Player
from model.tile import Tile
import application.utils.score as score_util


def pon(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 2 and not player.is_riichi and not player.agari:
        return True

    return False


def kan(player: Player, tile: Tile) -> bool:
    suit_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    count = len(suit_tiles)
    if count >= 3 and not player.is_riichi and not player.agari:
        return True

    return False


def ron(player: Player, tile: Tile, seat_wind: str, round_wind: str):
    player.hand.append(tile)
    result = score_util.agari(player, tile, [], seat_wind, round_wind)
    player.hand.pop(-1)
    if result.yaku is None or player.agari:
        return False
    return True


def tsumo(player: Player, seat_wind: str, round_wind: str):
    result = score_util.agari(player, player.tsumo, [], seat_wind, round_wind)
    if result.yaku is not None:
        return True
    return False


def riichi(player: Player) -> bool:
    all_tiles = player.hand[:]
    all_tiles.append(player.tsumo)
    shanten = score_util.shanten(all_tiles)
    if player.call == [] and shanten <= 0:
        return True
    return False
