from typing import List

from model.hand import Hand
from model.tile import Tile


def get_all_tiles(hand: Hand) -> List[Tile]:
    all_tiles = hand.tiles.copy()
    if hand.calls:
        for call in hand.calls:
            all_tiles.extend(call.tiles[:3])
    if hand.tsumo:
        all_tiles.append(hand.tsumo)

    return all_tiles


def update_hand(hand: Hand, discard_tile_id: int) -> Tile:
    remove_tile = next((tile for tile in hand.tiles
                        if tile.id == discard_tile_id),
                       None)
    if remove_tile is None:
        remove_tile = hand.tsumo
        hand.tsumo = None
    else:
        hand.tiles = list(filter(lambda t: t.id != remove_tile.id, hand.tiles))
        if hand.tsumo:
            hand.tiles.append(hand.tsumo)
            hand.tsumo = None

    return remove_tile
