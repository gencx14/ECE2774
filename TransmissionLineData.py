from Geometry import Geometry
import math


class TransmissionLineData:

    def __init__(self, name, bundle_num, line_geometry: Geometry, gmr, diam, d, rac):
        self.name = name
        self.n = bundle_num
        self.line_geometry = line_geometry
        self.Dab = self.line_geometry.Dab   # these distances should be in feet
        self.Dbc = self.line_geometry.Dbc
        self.Dca = self.line_geometry.Dca
        self.d = d                  # distance between conductors in a bundle
        self.GMR = gmr              # GMR of conductor in feet
        self.r = diam/12/2          # radius of conductor in feet
        self.R = rac/self.n         # resistance Ohms / mile

        self.w = 2*math.pi*60       # omega in rad/s
        self.Deq = math.sqrt(self.Dab * self.Dbc * self.Dca)        # Deq in feet

        match self.n:
            case 1:
                self.DSL = self.GMR
                self.DSC = self.r
            case 2:
                self.DSL = math.sqrt(self.d * self.GMR)
                self.DSC = math.sqrt(self.d * self.r)
            case 3:
                self.DSL = math.cbrt(self.d**2 * self.GMR)
                self.DSC = math.cbrt(self.d**2 * self.r)
            case 4:
                self.DSL = 1.0941 * math.sqrt(math.sqrt(self.d**3 * self.GMR))
                self.DSC = 1.0941 * math.sqrt(math.sqrt(self.d**3 * self.r))

        self.C_prime = 2 * math.pi * (8.854*10**-12) / math.log(self.Deq/self.DSC)      # in F/m
        self.L_prime = 2 * 10**-7 * math.log10(self.Deq/self.DSL)                       # in H/m

        self.C = self.C_prime * 1609        # in F/mile
        self.L = self.L_prime * 1609        # in H/mile
