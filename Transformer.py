from TransformerData import TransformerData
import math


class Transformer:

    j = math.sqrt(-1)

    def __init__(self, name: str, data: TransformerData):
        self.name = name
        self.data = data
        self.y = 1/(data.R + (Transformer.j*data.X))        # Admittance of transformer


