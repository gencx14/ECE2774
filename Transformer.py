from TransformerData import TransformerData
import math


class Transformer:

    j = math.sqrt(-1)

    def __init__(self, name: str, data: TransformerData, bus1, bus2):
        self.name = name
        self.data = data
        self.bus1 = bus1
        self.bus2 = bus2
        self.y = 1/(data.R + (Transformer.j*data.X))        # Admittance of transformer


