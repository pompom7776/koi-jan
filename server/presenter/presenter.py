import usecase.utils
from model.hand import Hand, CallTiles, TileFromPlayer
from model.player import Player
from model.room import Room
from model.table import Table


def room_to_dict(room: Room):
    players = [player_to_dict(p) for p in room.players]
    return {
        "room_id": room.room_id,
        "players": players,
        "table": table_to_dict(room.table),
        "current_player": room.current_player,
        "turn": room.turn
    }


def player_to_dict(player: Player):
    discarded_tiles = [t.__dict__ for t in player.discarded_tiles]
    selected_tiles = [t.__dict__ for t in player.selected_tiles]

    return {
        "id": player.id,
        "socket_id": player.socket_id,
        "name": player.name,
        "room_id": player.room_id,
        "is_riichi": player.is_riichi,
        "score": player.score,
        "score_info": player.score_info.__dict__,
        "round_score": player.round_score,
        "seat_wind": player.seat_wind,
        "hand": hand_to_dict(player.hand),
        "discarded_tiles": discarded_tiles,
        "selected_tiles": selected_tiles,
        "voted": player.voted,
    }


def table_to_dict(table: Table):
    dora = [t.__dict__.copy() for t in table.wall.dora]
    ura_dora = [t.__dict__.copy() for t in table.wall.ura_dora]
    for i in range(table.wall.dora_num, len(table.wall.dora)):
        dora[i]["name"] = "-"
        ura_dora[i]["name"] = "-"

    return {
        "round": table.round,
        "round_wind": table.round_wind,
        "dealer": table.dealer,
        "wall_num": len(table.wall.tiles),
        "dora": dora,
        "ura_dora": ura_dora,
        "seat_winds": table.seat_winds.__dict__
    }


def hand_to_dict(hand: Hand):
    hand.tiles = usecase.utils.sort_tiles_by_id(hand.tiles)
    tiles = [t.__dict__ for t in hand.tiles]
    calls = [call_to_dict(call) for call in hand.calls]
    tsumo = hand.tsumo.__dict__ if hand.tsumo else None

    return {
        "tiles": tiles,
        "calls": calls,
        "tsumo": tsumo
    }


def call_to_dict(call: CallTiles):
    call.tiles = usecase.utils.sort_tiles_by_id()
    tiles = [t.__dict__ for t in call.tiles]
    from_tile = from_tile_to_dict(call.from_tile) if call.from_tile else None

    return {
        "type": call.tile_type,
        "tiles": tiles,
        "from_tile": from_tile
    }


def from_tile_to_dict(from_tile: TileFromPlayer):
    return {
        "tile": from_tile.tile.__dict__,
        "player_id": from_tile.player_id
    }
