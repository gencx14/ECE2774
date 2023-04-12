import cmath
from BaseValues import BaseValues


class TransformerData:
    txCount = 0

    def __init__(self, name: str, s_rated, v_primary, v_secondary, zpu_transformer, xr_ratio, bases: BaseValues):
        self.name = name
        self.srated = s_rated
        self.sbase = bases.pbase
        self.vprimary = v_primary
        self.vsecondary = v_secondary
        self.zpu_old = zpu_transformer
        self.xr_ratio = xr_ratio
        self.txZpu = None
        self.txXpu = None
        self.txRpu = None
        self.txZpu = None
        self.makepu()


    def makepu(self):  # is it vlow or v primary????
        self.zpu_new = self.zpu_old * self.sbase / self.srated
        self.zpu_phase = cmath.atan(self.xr_ratio)
        self.txRpu = self.zpu_new * cmath.cos(self.zpu_phase)
        self.txXpu = self.zpu_new * cmath.sin(self.zpu_phase)
        self.txZpu = complex(self.txRpu, self.txXpu)
        self.txYpu = 1 / self.txZpu


    """
        self.zPuRect = (zPCT / 100) * cmath.exp(cmath.atan(xrRatio) * 1j) * (
                    (vprim ** 2 / srated) / (vprim ** 2 / 100))
        self.zPUphasor = cmath.polar(self.zPuRect)
    """


    def gettxYpu(self):
        return self.txYpu

    def gettxRpu(self):
        return self.txRpu

    def gettxXpu(self):
        return self.txXpu
