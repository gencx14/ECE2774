class Conductor:
    def __init__(self, name: str, outerDiameter, gmr, rAC, ampacity=None):
        self.name = name
        self.diameter = outerDiameter
        self.gmr = gmr
        self.rAC = rAC  # this will get passed to bundle
        self.ampacity = ampacity

    def getdiameter(self):
        return self.diameter

    def getgmr(self):
        return self.gmr

    def getrAC(self):
        return self.rAC





