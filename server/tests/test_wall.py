import unittest
from tile import Tile
from wall import Wall


class TestWall(unittest.TestCase):

    def setUp(self):
        self.wall = Wall()
        self.wall.initialize()

    def test_add_tile(self):
        tile = Tile(37, "manzu", 9, "9m")
        self.wall.add_tile(tile)
        self.assertEqual(len(self.wall.tiles), 137)

    def test_shuffle(self):
        original_tiles = self.wall.tiles[:]
        self.wall.shuffle()
        self.assertNotEqual(self.wall.tiles, original_tiles)

    def test_draw_tile(self):
        initial_tile_count = len(self.wall.tiles)
        drawn_tile = self.wall.draw_tile()
        self.assertEqual(len(self.wall.tiles), initial_tile_count - 1)
        self.assertIsInstance(drawn_tile, Tile)

    def test_draw_from_empty_wall(self):
        self.wall.tiles.clear()
        with self.assertRaises(IndexError):
            self.wall.draw_tile()

    def test_initialize(self):
        self.wall.initialize()
        self.assertEqual(len(self.wall.tiles), 136)


if __name__ == "__main__":
    unittest.main()
