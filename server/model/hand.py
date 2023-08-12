from typing import List

from model.tile import Tile


class TileFromPlayer:
    def __init__(self, tile: Tile = None, player_id: int = 0):
        self.tile = tile
        self.player_id = player_id


class CallTiles:
    def __init__(
        self,
        tile_type: str = "",
        tiles: List[Tile] = None,
        from_tile: TileFromPlayer = None,
    ):
        self.tile_type = tile_type
        self.tiles = [] if tiles is None else tiles
        self.from_tile = from_tile


class Hand:
    def __init__(
        self,
        tiles: List[Tile] = None,
        calls: List[CallTiles] = None,
        tsumo: Tile = None
    ):
        self.tiles = [] if tiles is None else tiles
        self.calls = [] if calls is None else calls
        self.tsumo = tsumo
