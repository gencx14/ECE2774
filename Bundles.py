from ConductorData import ConductorData
import numpy as n
import math as m

class Bundles:
    def __init__(self, NumBundles: int, ConductorData: ConductorData, d: float):
        if NumBundles < 1 or NumBundles > 4:
            print("Invalid number of Bundles.")
        else:
            #Number of Bundles
            self.NumBundles: int = NumBundles

            #Spacing between Bundles
            self.d: float = d
            self.ConductorData: ConductorData = ConductorData

            #Conductor Resistance
            self.r = self.ConductorData.r

            #Conductor GMR
            self.GMR = self.ConductorData.GMR

            #Conductor Resistance Scaled by Number of Bundles
            self.R = ConductorData.R / self.NumBundles

            #Conductor DSL based on Number of Bundles
            self.DSL = Bundles.find_DSL(self)

            #Conductor DSC Based on Number of Bundles
            self.DSC = Bundles.find_DSC(self)

        #DSL Based on Bundle Number
        def find_DSL(self) -> float:

            #Bundle of 1
            if self.NumBundles == 1:
                DSL = self.GMR

            #Bundle of 2
            if self.NumBundles == 2:
                DSL = (self.GMR * self.d) ** (1/2)

            #Bundle of 3
            if self.NumBundles == 3:
                DSL = n.cbrt(self.GMR * (self.d ** 2))

            #Bundle of 4
            if self.NumBundles == 4:
                DSL = 1.0941 * m.pow((self.GMR * (self.d ** 3)), (0.25))

            return DSL

        #DSC Based on Bundle Number
        def find_DSC(self) -> float:

            #Bundle of 1
            if self.NumBundles == 1:
                DSC = self.r

            # Bundle of 2
            if self.NumBundles == 2:
                DSC = m.sqrt(self.r * self.d)

            # Bundle of 3
            if self.NumBundles == 3:
                DSC = n.cbrt(self.r * (self.d ** 2))

            # Bundle of 4
            if self.NumBundles == 4:
                DSC = 1.0941 * m.pow((self.r * (self.d ** 3)), (0.25))

            return DSC