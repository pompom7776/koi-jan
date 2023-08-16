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
