import repository.player
import repository.tile
from model.player import Player
from model.tile import Tile
from model.tiles import Tiles


def register_player(player_name: str, socket_id: str) -> Player:
    player_id = repository.player.create_player(player_name, socket_id)
    player = repository.player.fetch_player(player_id)

    return player


def get_player_by_socket_id(socket_id: str) -> Player:
    player = repository.player.fetch_player_by_socket_id(socket_id)

    return player


def discard_tile(round_id: int, player_id: int, tile_id: int) -> Tile:
    repository.player.discard_tile(round_id, player_id, tile_id)
    tile = repository.tile.fetch_tile(tile_id)

    return tile


def get_discarded_tiles(round_id: int, player_id: int) -> Tiles:
    discarded = repository.player.fetch_discarded_tiles(round_id, player_id)
    return discarded
