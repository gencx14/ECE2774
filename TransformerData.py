import math


class TransformerData:

    def __init__(self, name, p_rated, v_rated_high, v_rated_low, z_pu_old, x_r):
        self.name = name
        self.p_rated = p_rated
        self.v_rated_high = v_rated_high
        self.v_rated_low = v_rated_low
        self.z_pu_new = z_pu_old * (100/p_rated)
        self.x_r = x_r

        self.z_angle = math.atan(self.x_r)
        self.R = self.z_pu_new * math.cos(self.z_angle)
        self.X = self.z_pu_new * math.sin(self.z_angle)
