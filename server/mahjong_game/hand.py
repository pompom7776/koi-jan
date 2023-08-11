from typing import List

from mahjong_game.tile import Tile
from mahjong_game import utils


class TileFromPlayer:
    def __init__(self, tile: Tile = None, player_id: int = 0):
        self.tile = tile
        self.player_id = player_id

    def to_dict(self):
        return {
            "tile": self.tile.__dict__,
            "player_id": self.player_id
        }


class CallTiles:
    def __init__(
            self,
            _type: str = "",
            tiles: List[Tile] = [],
            from_tile: TileFromPlayer = None):
        self.type = _type
        self.tiles = tiles
        self.from_tile = from_tile

    def to_dict(self):
        self.tiles = utils.sort_tiles_by_id(self.tiles)
        tiles = [tile.__dict__ for tile in self.tiles]
        from_tile_dict = self.from_tile.to_dict() if self.from_tile else None

        return {
            "type": self.type,
            "tiles": tiles,
            "from_tile": from_tile_dict
        }


class Hand:
    def __init__(
            self,
            tiles: List[Tile] = None,
            calls: List[CallTiles] = None,
            tsumo: Tile = None):
        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles
        if calls is None:
            self.calls = []
        else:
            self.calls = calls
        self.tsumo = tsumo

    def __eq__(self, other):
        return (self.tiles == other.tiles and
                self.calls == other.calls and
                self.tsumo == other.tsumo)

    def update_tsumo(self, tsumo: Tile):
        self.tsumo = tsumo

    def update_hand(self, discard_tile_id: int):
        remove_tile = None
        # 削除する牌が手牌にある場合
        remove_tile = next((tile for tile in self.tiles
                            if tile.id == discard_tile_id),
                           None)

        if remove_tile is None:
            remove_tile = self.tsumo
            self.tsumo = None

        else:
            self.tiles = list(
                filter(lambda t: t.id != remove_tile.id, self.tiles))
            if self.tsumo:
                self.tiles.append(self.tsumo)
                self.tsumo = None

        return remove_tile

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def get_all_tiles(self) -> List[Tile]:
        all_tiles = self.tiles.copy()

        if self.calls:
            for call in self.calls:
                all_tiles.extend(call.tiles)

        if self.tsumo:
            all_tiles.append(self.tsumo)

        return all_tiles

    def can_chi(self, tile: Tile) -> bool:
        suit_tiles = [t for t in self.tiles if t.suit == tile.suit]
        if (tile.rank <= 7 and
            tile.rank + 1 in [t.rank for t in suit_tiles] and
                tile.rank + 2 in [t.rank for t in suit_tiles]):
            return True
        elif (tile.rank >= 2 and
              tile.rank - 1 in [t.rank for t in suit_tiles] and
              tile.rank + 1 in [t.rank for t in suit_tiles]):
            return True
        elif (tile.rank >= 3 and
              tile.rank - 1 in [t.rank for t in suit_tiles] and
              tile.rank - 2 in [t.rank for t in suit_tiles]):
            return True

        return False

    def can_pon(self, tile: Tile) -> bool:
        suit_tiles = [t for t in self.tiles if t.suit ==
                      tile.suit and t.rank == tile.rank]
        count = len(suit_tiles)
        if count >= 2:
            return True

        return False

    def can_kan(self, tile: Tile) -> bool:
        suit_tiles = [t for t in self.tiles if t.suit ==
                      tile.suit and t.rank == tile.rank]
        count = len(suit_tiles)
        if count >= 3:
            return True

        return False

    def to_dict(self):
        self.tiles = utils.sort_tiles_by_id(self.tiles)
        tiles = [tile.__dict__ for tile in self.tiles]
        calls = [call.to_dict() for call in self.calls]
        tsumo = self.tsumo.__dict__ if self.tsumo else None

        return {
            "tiles": tiles,
            "calls": calls,
            "tsumo": tsumo
        }

    def __str__(self):
        tiles = self.get_all_tiles()
        sorted_tiles = utils.sort_tiles_by_id(tiles)
        return f"tiles: {', '.join(tile.name for tile in sorted_tiles)}"
