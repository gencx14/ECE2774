import numpy as n
import math as m

class Geometry:
    def __init__(self, PhaseA_X: float, PhaseA_Y: float, PhaseB_X: float, PhaseB_Y: float, PhaseC_X: float, PhaseC_Y: float):
        #X and Y Positions for Phases A, B, C
        self.PhaseA_X: float = PhaseA_X
        self.PhaseA_Y: float = PhaseA_Y
        self.PhaseB_X: float = PhaseB_X
        self.PhaseB_Y: float = PhaseB_Y
        self.PhaseC_X: float = PhaseC_X
        self.PhaseC_Y: float = PhaseC_Y

        self.DEQ = Geometry.find_DEQ(self)

    #Find Equivalent Distance, DEQ
    def find_DEQ(self):

        #Distance Between Phase AB, X
        Dab_X = self.PhaseA_X - self.PhaseB_X
        #Distance Between Phase AB, Y
        Dab_Y = self.PhaseA_Y - self.PhaseB_Y
        #Distance Between Phase AB
        Dab = m.sqrt(Dab_X ** 2) + (Dab_Y ** 2)

        #Distance Between Phase BC, X
        Dbc_X = self.PhaseB_X - self.PhaseC_X
        #Distance Between Phase BC, Y
        Dbc_Y = self.PhaseB_Y - self.PhaseC_Y
        #Distance Between Phase AB
        Dbc = m.sqrt(Dbc_X ** 2) + (Dbc_Y ** 2)

        #Distance Between Phase CA, X
        Dca_X = self.PhaseC_X - self.PhaseA_X
        #Distance Between Phase CA, Y
        Dca_Y = self.PhaseC_Y - self.PhaseA_Y
        #Distance Between Phase CA
        Dca = m.sqrt(Dca_X ** 2) + (Dca_Y ** 2)

        #Equivalent Distance
        DEQ = n.cbrt(Dab * Dbc * Dca)
        return DEQ