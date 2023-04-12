import cmath
class BaseValues:
    def __init__(self, pbase, vbase):
        self.pbase = pbase
        self.vbase = vbase
        self.zbase = self.vbase**2/self.pbase
        self.ybase = 1 / self.zbase

