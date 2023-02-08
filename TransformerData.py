import math


class TransformerData:

    def __init__(self, p_rated, v_rated_high, v_rated_low, z_pct, x_r):
        self.p_rated = p_rated
        self.v_rated_high = v_rated_high
        self.v_rated_low = v_rated_low
        self.z_pct = z_pct
        self.x_r = x_r

        self.z_angle = math.atan(self.x_r) * ((self.v_rated_low**2/self.p_rated)/(self.v_rated_low**2/100))
        self.R = self.z_pct/100 * math.cos(self.z_angle)
        self.X = self.z_pct/100 * math.sin(self.z_angle)
