import unittest
from mahjong_game.tile import Tile
from mahjong_game.player import Player
from mahjong_game.hand import Hand


class TestPlayer(unittest.TestCase):
    def test_player_attributes(self):
        p1 = Player("socket_id", "Player 1", 9999)
        p2 = Player("socket_id", "Player 2", 9999)
        p3 = Player("socket_id", "Player 3", 9999)
        p4 = Player("socket_id", "Player 4", 9999)

        self.assertEqual(p1.id, 1)
        self.assertEqual(p2.id, 2)
        self.assertEqual(p3.id, 3)
        self.assertEqual(p4.id, 4)

        self.assertEqual(p1.name, "Player 1")
        self.assertEqual(p1.score, 0)
        self.assertIsInstance(p1.hand, Hand)
        self.assertEqual(p1.seat_wind, "")
        self.assertEqual(p1.discarded_tiles, [])
        self.assertFalse(p1.is_riichi)

    def test_update_score(self):
        p = Player("socket_id", "Player", 9999)
        p.update_score(1000)
        self.assertEqual(p.score, 1000)

    def test_update_discarded_tiles(self):
        p = Player("socket_id", "Player", 9999)
        tile1 = Tile(1, "manzu", 1, "1m")
        tile2 = Tile(2, "pinzu", 2, "2p")

        p.update_discrded_tiles(tile1)
        self.assertEqual(len(p.discarded_tiles), 1)
        self.assertEqual(p.discarded_tiles[0], tile1)

        p.update_discrded_tiles(tile2)
        self.assertEqual(len(p.discarded_tiles), 2)
        self.assertEqual(p.discarded_tiles[1], tile2)

    def test_update_seat_wind(self):
        p = Player("socket_id", "Player", 9999)

        p.update_seat_wind("東")
        self.assertEqual(p.seat_wind, "東")

        p.update_seat_wind("南")
        self.assertEqual(p.seat_wind, "南")

        p.update_seat_wind("西")
        self.assertEqual(p.seat_wind, "西")

        p.update_seat_wind("北")
        self.assertEqual(p.seat_wind, "北")

        with self.assertRaises(ValueError):
            p.update_seat_wind("hoge")

    def test_riichi(self):
        p = Player("socket_id", "Player", 9999)
        self.assertFalse(p.is_riichi)

        p.riichi()
        self.assertTrue(p.is_riichi)

    def test_reset_riichi(self):
        p = Player("socket_id", "Player", 9999)
        p.riichi()
        self.assertTrue(p.is_riichi)

        p.reset_riichi()
        self.assertFalse(p.is_riichi)


if __name__ == "__main__":
    unittest.main()
