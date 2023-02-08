from Transformer import Transformer
from Bus import Bus
from Generator import Generator
from TransmissionLine import TransmissionLine


class Network:
    def __init__(self, name: str):
        self.name: str = name

