from TransformerData import TransformerData
from Bus import Bus
import pandas as pd


class Transformer:
    # you will need to have already created a tx data object to pass into this class.
    def __init__(self, name: str, bus1: Bus, bus2: Bus, tx_data: TransformerData):
        self.y = None
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.buses = [self.bus1, self.bus2]
        self.data = tx_data
        self.calc_y()

    def calc_y(self):
        ypu_df = pd.DataFrame()
        ypu_df.loc[self.bus1, self.bus1] = self.data.txYpu
        ypu_df.loc[self.bus1, self.bus2] = -1 * self.data.txYpu
        ypu_df.loc[self.bus2, self.bus1] = -1 * self.data.txYpu
        ypu_df.loc[self.bus2, self.bus2] = self.data.txYpu
        #  check to see if this saves y as a variable
        self.y = ypu_df
