from typing import List

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH

# from hand import CallTiles, TileFromPlayer
from mahjong_game.hand import Hand
from mahjong_game.tile import Tile
from mahjong_game import utils


class Score:
    def __init__(self, result=None):
        if result is None or result.error:
            self.han = 0
            self.fu = 0
            self.cost = 0
            self.yaku = []
        else:
            self.han = result.han
            self.fu = result.fu
            self.cost = result.cost['main'] + result.cost['additional'] * 2
            self.yaku = [yaku.name for yaku in result.yaku]


def convert_136_tile(tile: Tile):
    man = ''
    pin = ''
    sou = ''
    # honors = 1-4:east, south, west, north  5-7: white, green, red
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
    # honors = 1-4:east, south, west, north  5-7: white, green, red
    honors = ''

    sorted_tiles = utils.sort_tiles_by_id(tiles)
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


def convert_34_tiles(tiles: List[Tile]):
    man = ''
    pin = ''
    sou = ''
    # honors = 1-4:east, south, west, north  5-7: white, green, red
    honors = ''

    sorted_tiles = utils.sort_tiles_by_id(tiles)
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


def shanten(hand: List):
    char_tiles = convert_34_tiles(hand)

    shanten = Shanten()

    return shanten.calculate_shanten(char_tiles)


def agari(hand: Hand,
          win_tile: Tile,
          dora: List[Tile],
          round_wind: str,
          seat_wind: str,
          is_tsumo: bool,
          is_riichi: bool):
    tiles = hand.get_all_tiles()
    char_tiles = convert_136_tiles(tiles)

    win_tile = convert_136_tile(win_tile)

    calculator = HandCalculator()

    if hand.calls != []:
        melds = [
            Meld(Meld.PON, convert_136_tiles(call.tiles))
            for call in hand.calls
        ]
    else:
        melds = None

    print(melds)
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
                                            win_tile,
                                            melds,
                                            dora_indicators,
                                            config)

    return Score(result)
