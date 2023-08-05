import unittest
from tile import Tile
from hand import CallTiles, TileFromPlayer, Hand


class TestHand(unittest.TestCase):
    def test_hand_attributes(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'green')
        tile_11 = Tile(130, 'dragon', 2, 'green')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')

        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        hand = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=tile_11
        )

        self.assertEqual(hand.tiles,
                         [tile_1, tile_2, tile_3, tile_4, tile_5,
                          tile_6, tile_7, tile_8, tile_9, tile_10])
        for call in hand.calls:
            self.assertEqual(call.tiles,
                             [call_tile_1, call_tile_2, call_tile_3])
            self.assertEqual(call.from_tile.tile, call_tile_2)
        self.assertEqual(hand.tsumo, tile_11)

    def test_get_all_tiles(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'green')
        tile_11 = Tile(130, 'dragon', 2, 'green')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')
        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=tile_11
        )

        expected_tiles = [tile_1, tile_2, tile_3, tile_4, tile_5,
                          tile_6, tile_7, tile_8, tile_9, tile_10,
                          call_tile_1, call_tile_2, call_tile_3, tile_11]

        all_tiles = h.get_all_tiles()

        self.assertCountEqual(all_tiles, expected_tiles)

    # def test_to_dict(self):
    #     tile_1 = Tile(1, 'manzu', 1, '1m')
    #     tile_2 = Tile(5, 'manzu', 2, '2m')
    #     tile_3 = Tile(9, 'manzu', 3, '3m')
    #     tile_4 = Tile(61, 'pinzu', 7, '7p')
    #     tile_5 = Tile(65, 'pinzu', 8, '8p')
    #     tile_6 = Tile(69, 'pinzu', 9, '9p')
    #     tile_7 = Tile(109, 'wind', 1, 'east')
    #     tile_8 = Tile(110, 'wind', 1, 'east')
    #     tile_9 = Tile(111, 'wind', 1, 'east')
    #     tile_10 = Tile(129, 'dragon', 2, 'green')
    #     tile_11 = Tile(130, 'dragon', 2, 'green')
    #
    #     call_tile_1 = Tile(73, 'souzu', 1, '1s')
    #     call_tile_2 = Tile(77, 'souzu', 2, '2s')
    #     call_tile_3 = Tile(81, 'souzu', 3, '3s')
    #
    #     call_tiles = CallTiles(
    #         "chi",
    #         [call_tile_1, call_tile_2, call_tile_3],
    #         TileFromPlayer(call_tile_2, 1))
    #
    #     h = Hand(
    #         tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
    #                tile_6, tile_7, tile_8, tile_9, tile_10],
    #         calls=[call_tiles],
    #         tsumo=tile_11
    #     )
    #
    #     expected_dict = {
    #         'tiles': [
    #             {'id': 1, 'suit': 'manzu', 'rank': 1,
    #                 'name': '1m', 'bonus': False},
    #             {'id': 5, 'suit': 'manzu', 'rank': 2,
    #                 'name': '2m', 'bonus': False},
    #             {'id': 9, 'suit': 'manzu', 'rank': 3,
    #                 'name': '3m', 'bonus': False},
    #             {'id': 61, 'suit': 'pinzu', 'rank': 7,
    #                 'name': '7p', 'bonus': False},
    #             {'id': 65, 'suit': 'pinzu', 'rank': 8,
    #                 'name': '8p', 'bonus': False},
    #             {'id': 69, 'suit': 'pinzu', 'rank': 9,
    #                 'name': '9p', 'bonus': False},
    #             {'id': 109, 'suit': 'wind', 'rank': 1,
    #              'name': 'east', 'bonus': False},
    #             {'id': 110, 'suit': 'wind', 'rank': 1,
    #              'name': 'east', 'bonus': False},
    #             {'id': 111, 'suit': 'wind', 'rank': 1,
    #              'name': 'east', 'bonus': False},
    #             {'id': 129, 'suit': 'dragon', 'rank': 2,
    #              'name': 'green', 'bonus': False}
    #
    #         ],
    #         'calls': [
    #             {
    #                 'type': 'chi',
    #                 'tiles': [
    #                     {'id': 73, 'suit': 'souzu', 'rank': 1,
    #                      'name': '1s', 'bonus': False},
    #                     {'id': 77, 'suit': 'souzu', 'rank': 2,
    #                      'name': '2s', 'bonus': False},
    #                     {'id': 81, 'suit': 'souzu', 'rank': 3,
    #                      'name': '3s', 'bonus': False}
    #                 ],
    #                 'from_tile': {
    #                     'tile': {'id': 77, 'suit': 'souzu', 'rank': 2,
    #                              'name': '2s', 'bonus': False},
    #                     'player_id': 1
    #                 }
    #             }
    #         ],
    #         'tsumo': {'id': 130, 'suit': 'dragon', 'rank': 2,
    #                   'name': 'green', 'bonus': False}
    #     }
    #
    #     self.assertEqual(h.to_dict(), expected_dict)

    def test_update_tsumo(self):
        tsumo = Tile(6, 'manzu', 6, '6m')

        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'dragon')
        tile_11 = Tile(130, 'dragon', 2, 'dragon')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')

        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=None
        )

        h.update_tsumo(tsumo)

        self.assertEqual(h.tsumo, tsumo)

    def test_update_hand_tsumo(self):
        discard_tile = Tile(130, 'dragon', 2, 'green')

        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'green')
        tile_11 = Tile(130, 'dragon', 2, 'green')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')

        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=tile_11
        )

        h.update_hand(discard_tile)

        expected_hand = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=None
        )

        self.assertEqual(h, expected_hand)

    def test_update_hand_tiles(self):
        discard_tile = Tile(1, 'manzu', 1, '1m')

        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'green')
        tile_11 = Tile(130, 'dragon', 2, 'green')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')

        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=tile_11
        )

        h.update_hand(discard_tile.id)

        expected_hand = Hand(
            tiles=[tile_2, tile_3, tile_4, tile_5, tile_6,
                   tile_7, tile_8, tile_9, tile_10, tile_11],
            calls=[call_tiles],
            tsumo=None
        )

        self.assertEqual(h, expected_hand)

    def test_can_chi(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(85, 'souzu', 4, '4s')
        tile_8 = Tile(89, 'souzu', 5, '5s')
        tile_9 = Tile(93, 'souzu', 6, '6s')
        tile_10 = Tile(109, 'wind', 1, 'east')
        tile_11 = Tile(110, 'wind', 1, 'east')
        tile_12 = Tile(111, 'wind', 1, 'east')
        tile_13 = Tile(129, 'dragon', 2, 'green')

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5, tile_6,
                   tile_7, tile_8, tile_9, tile_10, tile_11, tile_12, tile_13],
            calls=[],
            tsumo=None
        )

        # 1mで順子を作ることができる
        call_tile = Tile(2, 'manzu', 1, '1m')
        self.assertTrue(h.can_chi(call_tile))
        # 3mで順子を作ることができる
        call_tile = Tile(9, 'manzu', 3, '3m')
        self.assertTrue(h.can_chi(call_tile))

        # 7pで順子を作ることができる
        call_tile = Tile(62, 'pinzu', 7, '7m')
        self.assertTrue(h.can_chi(call_tile))

        # 9pで順子を作ることができる
        call_tile = Tile(70, 'pinzu', 9, '9m')
        self.assertTrue(h.can_chi(call_tile))

        # 3sで順子を作ることができる
        call_tile = Tile(81, 'souzu', 4, '3s')
        self.assertTrue(h.can_chi(call_tile))

        # 7sで順子を作ることができる
        call_tile = Tile(97, 'souzu', 5, '5s')
        self.assertTrue(h.can_chi(call_tile))

        # 5mで順子を作ることができない
        call_tile = Tile(17, 'manzu', 5, '5m')
        self.assertFalse(h.can_chi(call_tile))

    def test_can_pon(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(2, 'manzu', 1, '1m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(85, 'souzu', 4, '4s')
        tile_8 = Tile(89, 'souzu', 5, '5s')
        tile_9 = Tile(93, 'souzu', 6, '6s')
        tile_10 = Tile(109, 'wind', 1, 'east')
        tile_11 = Tile(110, 'wind', 1, 'east')
        tile_12 = Tile(111, 'wind', 1, 'east')
        tile_13 = Tile(129, 'dragon', 2, 'green')

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5, tile_6,
                   tile_7, tile_8, tile_9, tile_10, tile_11, tile_12, tile_13],
            calls=[],
            tsumo=None
        )

        # 1mで刻子を作ることができる
        call_tile = Tile(3, 'manzu', 1, '1m')
        self.assertTrue(h.can_pon(call_tile))
        # eastで刻子を作ることができる
        call_tile = Tile(112, 'wind', 1, 'east')
        self.assertTrue(h.can_pon(call_tile))

        # greenで刻子を作ることができない
        call_tile = Tile(129, 'dragon', 2, 'green')
        self.assertFalse(h.can_pon(call_tile))

    def test_can_kan(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(2, 'manzu', 1, '1m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(85, 'souzu', 4, '4s')
        tile_8 = Tile(89, 'souzu', 5, '5s')
        tile_9 = Tile(93, 'souzu', 6, '6s')
        tile_10 = Tile(109, 'wind', 1, 'east')
        tile_11 = Tile(110, 'wind', 1, 'east')
        tile_12 = Tile(111, 'wind', 1, 'east')
        tile_13 = Tile(129, 'dragon', 2, 'green')

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5, tile_6,
                   tile_7, tile_8, tile_9, tile_10, tile_11, tile_12, tile_13],
            calls=[],
            tsumo=None
        )

        # 1mで槓子を作ることができない
        call_tile = Tile(3, 'manzu', 1, '1m')
        self.assertFalse(h.can_kan(call_tile))
        # eastで槓子を作ることができる
        call_tile = Tile(112, 'wind', 1, 'east')
        self.assertTrue(h.can_kan(call_tile))

        # greenで槓子を作ることができない
        call_tile = Tile(129, 'dragon', 2, 'green')
        self.assertFalse(h.can_kan(call_tile))

    def test_str_method(self):
        tile_1 = Tile(1, 'manzu', 1, '1m')
        tile_2 = Tile(5, 'manzu', 2, '2m')
        tile_3 = Tile(9, 'manzu', 3, '3m')
        tile_4 = Tile(61, 'pinzu', 7, '7p')
        tile_5 = Tile(65, 'pinzu', 8, '8p')
        tile_6 = Tile(69, 'pinzu', 9, '9p')
        tile_7 = Tile(109, 'wind', 1, 'east')
        tile_8 = Tile(110, 'wind', 1, 'east')
        tile_9 = Tile(111, 'wind', 1, 'east')
        tile_10 = Tile(129, 'dragon', 2, 'green')
        tile_11 = Tile(130, 'dragon', 2, 'green')

        call_tile_1 = Tile(73, 'souzu', 1, '1s')
        call_tile_2 = Tile(77, 'souzu', 2, '2s')
        call_tile_3 = Tile(81, 'souzu', 3, '3s')

        call_tiles = CallTiles(
            "chi",
            [call_tile_1, call_tile_2, call_tile_3],
            TileFromPlayer(call_tile_2, 1))

        h = Hand(
            tiles=[tile_1, tile_2, tile_3, tile_4, tile_5,
                   tile_6, tile_7, tile_8, tile_9, tile_10],
            calls=[call_tiles],
            tsumo=tile_11
        )

        expected_str = "tiles: 1m, 2m, 3m, 7p, 8p, 9p, 1s, 2s, 3s, east, east, east, green, green"

        self.assertEqual(str(h), expected_str)


if __name__ == '__main__':
    unittest.main()
