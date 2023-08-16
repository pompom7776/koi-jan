from typing import List

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH

import usecase.utils
import usecase.hand
from model.hand import Hand
from model.tile import Tile
from model.score import Score


def shanten(tiles: List[Tile]):
    char_tiles = convert_34_tiles(tiles)
    shanten = Shanten()
    return shanten.calculate_shanten(char_tiles)


def agari(hand: Hand,
          win_tile: Tile,
          dora: List[Tile],
          round_wind: str,
          seat_wind: str,
          is_tsumo: bool,
          is_riichi: bool):
    tiles = usecase.hand.get_all_tiles(hand)
    char_tiles = convert_136_tiles(tiles)
    char_win_tile = convert_136_tile(win_tile)

    calculator = HandCalculator()

    if hand.calls != []:
        melds = []
        pons = [
            Meld(Meld.PON, convert_136_tiles(call.tiles))
            for call in hand.calls if call.tile_type == "pon"
        ]
        melds.extend(pons)
        kans = [
            Meld(Meld.KAN, convert_136_tiles(call.tiles))
            for call in hand.calls if call.tile_type == "dai_min_kan"
        ]
        melds.extend(kans)
    else:
        melds = None

    dora_indicators = [convert_136_tile(t) for t in dora]

    winds = {
        "east": EAST,
        "south": SOUTH,
        "west": WEST,
        "north": NORTH
    }

    config = HandConfig(is_tsumo=is_tsumo,
                        is_riichi=is_riichi,
                        player_wind=winds[seat_wind],
                        round_wind=winds[round_wind],
                        options=OptionalRules(has_open_tanyao=True))

    result = calculator.estimate_hand_value(char_tiles,
                                            char_win_tile,
                                            melds,
                                            dora_indicators,
                                            config)

    return Score(result)


def convert_34_tiles(tiles: List[Tile]):
    man = ''
    pin = ''
    sou = ''
    # honors = 1-4: east, south, west, north
    #          5-7: white, green, red
    honors = ''

    sorted_tiles = usecase.utils.sort_tiles_by_id(tiles)
    for tile in sorted_tiles:
        if tile.suit == "manzu":
            man += str(tile.rank)
        if tile.suit == "pinzu":
            pin += str(tile.rank)
        if tile.suit == "souzu":
            sou += str(tile.rank)
        if tile.suit == "wind":
            honors += str(tile.rank)
        if tile.suit == "dragon":
            honors += str(tile.rank + 4)

    return TilesConverter.string_to_34_array(man=man,
                                             pin=pin,
                                             sou=sou,
                                             honors=honors)


def convert_136_tile(tile: Tile):
    man = ''
    pin = ''
    sou = ''
    # honors = 1-4: east, south, west, north
    #          5-7: white, green, red
    honors = ''

    if tile.suit == "manzu":
        man += str(tile.rank)
    if tile.suit == "pinzu":
        pin += str(tile.rank)
    if tile.suit == "souzu":
        sou += str(tile.rank)
    if tile.suit == "wind":
        honors += str(tile.rank)
    if tile.suit == "dragon":
        honors += str(tile.rank + 4)

    return TilesConverter.string_to_136_array(man=man,
                                              pin=pin,
                                              sou=sou,
                                              honors=honors)[0]


def convert_136_tiles(tiles: List[Tile]):
    man = ''
    pin = ''
    sou = ''
    # honors = 1-4: east, south, west, north
    #          5-7: white, green, red
    honors = ''

    sorted_tiles = usecase.utils.sort_tiles_by_id(tiles)
    for tile in sorted_tiles:
        if tile.suit == "manzu":
            man += str(tile.rank)
        if tile.suit == "pinzu":
            pin += str(tile.rank)
        if tile.suit == "souzu":
            sou += str(tile.rank)
        if tile.suit == "wind":
            honors += str(tile.rank)
        if tile.suit == "dragon":
            honors += str(tile.rank + 4)

    return TilesConverter.string_to_136_array(man=man,
                                              pin=pin,
                                              sou=sou,
                                              honors=honors)
