import cmath
class Geometry:

    def __init__(self, name: str, ax, ay, bx, by, cx, cy):
        self.dab = cmath.sqrt((ax-bx)**2 - (ay - by)**2)
        self.dbc = cmath.sqrt((bx-cx)**2 - (by - cy)**2)
        self.dca = cmath.sqrt((cx - ax) ** 2 - (cy - ay) ** 2)
        self.deq = (self.dab * self.dbc * self.dca)**(1/2)

    def getdab(self):
        return self.dab

    def getdbc(self):
        return self.dbc

    def getdca(self):
        return self.dca

    def getdeq(self):
        return self.deq



