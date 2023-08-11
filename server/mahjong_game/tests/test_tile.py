# import unittest
# from mahjong_game.tile import Tile
#
#
# class TestTile(unittest.TestCase):
#     def test_tile_string_representation(self):
#         tile1 = Tile(1, 'manzu', 1, '1m')
#         tile2 = Tile(53, 'pinzu', 5, '5p', True)
#         tile3 = Tile(109, 'wind', 1, 'east')
#         tile4 = Tile(129, 'dragon', 2, 'green')
#
#         # テストケース1
#         expected_str1 = "id: 1, suit: manzu, rank: 1, name: 1m, bonus: False"
#         self.assertEqual(str(tile1), expected_str1)
#
#         # テストケース2
#         expected_str2 = "id: 53, suit: pinzu, rank: 5, name: 5p, bonus: True"
#         self.assertEqual(str(tile2), expected_str2)
#
#         # テストケース3
#         expected_str3 = "id: 109, suit: wind, rank: 1, name: east, bonus: False"
#         self.assertEqual(str(tile3), expected_str3)
#
#         # テストケース4
#         expected_str4 = "id: 129, suit: dragon, rank: 2, name: green, bonus: False"
#         self.assertEqual(str(tile4), expected_str4)
#
#
# if __name__ == '__main__':
#     unittest.main()
