import cmath
from BaseValues import BaseValues
import warnings
import Constants

class TransformerData:
    txCount = 0

    def __init__(self, name: str, s_rated, v_primary, v_secondary, zpu_transformer, xr_ratio, bases: BaseValues, config: str, Zg_a, Zg_b):
        self.name = name
        self.srated = s_rated
        self.sbase = bases.pbase
        self.vprimary = v_primary
        self.vsecondary = v_secondary
        self.zpu_old = zpu_transformer
        self.xr_ratio = xr_ratio
        self.Zg_a = Zg_a
        if self.Zg_a == 0:
            self.Yg_a = Constants.INF
        else:
            self.Yg_a = 1 / self.Zg_a
        self.Zg_b = Zg_b
        if self.Zg_b == 0:
            self.Yg_b = Constants.INF
        else:
            self.Yg_b = 1 / Zg_b
        self.txZpu = None
        self.txXpu = None
        self.txRpu = None
        self.makepu()
        self.zPu = self.txZpu
        if config not in ["Y-Y", 'Y-D', 'D-Y', 'D-D']:
            warnings.warn("Transformer grounding/configuration not selected. Sequence Calculation not possible.\n"
                          "Please enter a string below to your transformer data to output accurate sequence information\n"
                          "\t 1. \"Y-Y\" = Wye/Wye\n"
                          "\t 2. \"Y-D\" = Wye/Delta\n"
                          "\t 3. \"D-D\" = Delta-Delta\n"
                          "\t 2. \"D-Y\" = Delta/Wye\n", TxConfigurationWarning)
        else:
            self.Txconfiguration = config
            self.sequenceZYcalc()


    def makepu(self):  # is it vlow or v primary????
        self.zpu_new = self.zpu_old * self.sbase / self.srated
        self.zpu_phase = cmath.atan(self.xr_ratio)
        self.txRpu = self.zpu_new * cmath.cos(self.zpu_phase)
        self.txXpu = self.zpu_new * cmath.sin(self.zpu_phase)
        self.txZpu = complex(self.txRpu, self.txXpu)
        self.txYpu = 1 / self.txZpu

    #calculates the sequence impedance and admittance to be used for sequence busses
    def sequenceZYcalc(self):
        self.z1 = self.txZpu
        self.z2 = self.txZpu
        self.y1 =1 / self.z1
        self.y2 = 1 / self.z2
        if self.Zg_a and self.Zg_b == Constants.INF:
            warnings.warn(f'INVALID: You have choosen {self.name} to have no ground reference', TxZgWarning)
        elif self.Zg_a == Constants.INF:
            self.z0aa = Constants.INF
            self.z0ab = Constants.INF
            self.z0bb = self.txZpu + 3 * self.Zg_b
        elif self.Zg_b == Constants.INF:
            self.z0aa = 3 * self.Zg_a + self.txZpu
            self.z0ab = Constants.INF
            self.z0bb = Constants.INF
        else:
            self.z0aa = 3 * self.Zg_a + self.txZpu + 3 * self.Zg_b
            self.z0ab = self.z0aa
            self.z0bb = self.z0ab
        self.y0aa = 1 / self.z0aa
        self.y0ab = 1 / self.z0ab
        self.y0bb = 1 / self.z0bb

        '''
        if self.Txconfiguration == "Y-Y":
            # Add Grounded Wye/Grounded Wye impedance values
            #z1a is the positvie sequence impedance seen at node A (or bus 1)
            self.z1aa = self.txZpu
            self.z1ab = self.z1aa
            self.z1ba = self.z1aa
            self.z1bb = self.z1aa
            self.z2aa = self.txZpu
            self.z2ab = self.z2aa
            self.z2ba = self.z2aa
            self.z2bb = self.z2aa
            self.z0aa = 3 * self.Zg_a + self.txZpu + 3 * self.Zg_b
            self.z0ab = self.z0aa
            self.z0ba = self.z0aa
            self.z0bb = self.z0aa
        elif self.Txconfiguration == 'D-Y':
            # Add Delta/Grounded Wye impedance values
            # How does the presence of the grounding effect this?
            self.z1aa = self.txZpu
            self.z1ab = self.z1aa
            self.z1ba = self.z1aa
            self.z1bb = self.z1aa
            self.z2aa = self.txZpu
            self.z2ab = self.z2aa
            self.z2ba = self.z2aa
            self.z2bb = self.z2aa
            self.z0aa = 0
            self.z0ab = 0
            self.z0ba = self.txZpu + 3 * self.Zg_b
            self.z0bb = self.txZpu + 3 * self.Zg_b
        elif self.Txconfiguration == 3:
            # Add Ungrounded Wye/Grounded Wye impedance values
            self.z1aa = self.txZpu
            self.z1ab = self.z1aa
            self.z1ba = self.z1aa
            self.z1bb = self.z1aa
            self.z2aa = self.txZpu
            self.z2ab = self.z2aa
            self.z2ba = self.z2aa
            self.z2bb = self.z2aa
            self.z0aa = 0
            self.z0ab = 0
            self.z0ba = self.txZpu + 3 * self.zg_b
            self.z0bb = self.txZpu + 3 * self.zg_b
        self.y1aa = 1 / self.z1aa
        self.y1ab = 1 / self.z1ab
        self.y1ba = 1 / self.z1ba
        self.y1ab = 1 / self.z1ab
        self.y1bb = 1 / self.z1bb
        self.y2aa = 1 / self.z2aa
        self.y2ab = 1 / self.z2ab
        self.y2ba = 1 / self.z2ba
        self.y2bb = 1 / self.z2bb
        self.y0aa = 1 / self.z0aa
        self.y0ab = 1 / self.z0ab
        self.y0ba = 1 / self.z0ba
        self.y0bb = 1 / self.z0bb '''



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
