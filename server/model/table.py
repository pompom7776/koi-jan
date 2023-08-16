from model.wall import Wall


class SeatWindPlayers:
    def __init__(self,
                 east: int = 0,
                 south: int = 0,
                 west: int = 0,
                 north: int = 0):
        self.east = east
        self.south = south
        self.west = west
        self.north = north


class Table:
    def __init__(self):
        self.round: int = 0
        self.round_wind: str = ""
        self.dealer: int = 0
        self.wall: Wall = Wall()
        self.seat_winds = SeatWindPlayers()
