import math


class Geometry:

    def __init__(self, name, x1, y1, x2, y2, x3, y3):
        self.name = name
        self.Dab_x = abs(x1-x2)
        self.Dab_y = abs(y1-y2)
        self.Dbc_x = abs(x2 - x3)
        self.Dbc_y = abs(y2-y3)
        self.Dca_x = abs(x1-x3)
        self.Dca_y = abs(y1-y3)
        self.Dab = math.sqrt(self.Dab_x**2 + self.Dab_y**2)
        self.Dbc = math.sqrt(self.Dbc_x**2 + self.Dbc_y**2)
        self.Dca = math.sqrt(self.Dca_x**2 + self.Dca_y**2)
