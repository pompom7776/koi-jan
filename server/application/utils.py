from model.player import Player
from model.tile import Tile


def sort_tiles_by_id(tiles):
    return sorted(tiles, key=lambda tile: tile.id)


def check_pon(player: Player, tile: Tile):
    same_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    if len(same_tiles) >= 2 and not player.is_riichi:
        return True
    return False


def check_kan(player: Player, tile: Tile):
    same_tiles = [t for t in player.hand
                  if t.suit == tile.suit and t.rank == tile.rank]
    if len(same_tiles) >= 3 and not player.is_riichi:
        return True
    return False
