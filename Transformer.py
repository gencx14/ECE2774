from TransformerData import TransformerData
from Bus import Bus
import pandas as pd


class Transformer:
    # you will need to have already created a tx data object to pass into this class.
    def __init__(self, name: str, bus1: Bus, bus2: Bus, tx_data: TransformerData):
        self.y = None
        self.y1 = None
        self.y2 = None
        self.y0 = None
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.buses = [self.bus1, self.bus2]
        self.data = tx_data
        self.zPu = self.data.zPu
        self.calc_y()
        self.calc_ysequence()

    def calc_y(self):
        ypu_df = pd.DataFrame()
        ypu_df.loc[self.bus1, self.bus1] = self.data.txYpu
        ypu_df.loc[self.bus1, self.bus2] = -1 * self.data.txYpu
        ypu_df.loc[self.bus2, self.bus1] = -1 * self.data.txYpu
        ypu_df.loc[self.bus2, self.bus2] = self.data.txYpu
        #  check to see if this saves y as a variable
        self.y = ypu_df

    # calculate positive sequence y bus for this transformer
    def calc_ysequence(self):
        y1pu_df = pd.DataFrame()
        y2pu_df = pd.DataFrame()
        y0pu_df = pd.DataFrame()

        # calculate positive sequence element y bus
        y1pu_df.loc[self.bus1, self.bus1] = self.data.y1
        y1pu_df.loc[self.bus1, self.bus2] = -1 * self.data.y1
        y1pu_df.loc[self.bus2, self.bus1] = -1 * self.data.y1
        y1pu_df.loc[self.bus2, self.bus2] = self.data.y1

        # calculate negative sequence element y bus
        y2pu_df.loc[self.bus1, self.bus1] = self.data.y2
        y2pu_df.loc[self.bus1, self.bus2] = -1 * self.data.y2
        y2pu_df.loc[self.bus2, self.bus1] = -1 * self.data.y2
        y2pu_df.loc[self.bus2, self.bus2] = self.data.y2

        # Calculate zero sequence element y bus
        y0pu_df.loc[self.bus1, self.bus1] = self.data.y0aa
        y0pu_df.loc[self.bus1, self.bus2] = -1 * self.data.y0ab
        y0pu_df.loc[self.bus2, self.bus1] = -1 * self.data.y0ab
        y0pu_df.loc[self.bus2, self.bus2] = self.data.y0bb

        #  Store the element y buses in the Transformer class
        self.y1 = y1pu_df
        self.y2 = y2pu_df
        self.y0 = y0pu_df


