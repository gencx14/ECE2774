import math
from Conductor import Conductor
class Bundle:
    def __init__(self, name, bundleSize, bundleDistance, conductor: Conductor):
        self.size = bundleSize
        self.bundleDistance = bundleDistance
        self.radius = (conductor.getdiameter() / 2) / 12
        #send bundle conductor data
        #calculate Dsl and Dsc in here

        if bundleSize == 1:
            self.dsl = conductor.getgmr()
            self.dsc = self.radius  #get radius
        elif bundleSize == 2:
            self.dsl = math.sqrt(conductor.getgmr() * self.bundleDistance)
            self.dsc = math.sqrt(self.radius * self.bundleDistance)
        elif bundleSize == 3:
            self.dsl = math.cbrt(conductor.getgmr() * self.bundleDistance**2)
            self.dsc = math.cbrt(self.radius * self.bundleDistance**2)
        elif bundleSize == 4:
            self.dsl = 1.0941 * (conductor.getgmr() * self.bundleDistance**3)**(1/4)
            self.dsc = 1.0941 * (self.radius * self.bundleDistance**3)**(1/4)
        else:
            print("This program can only handle bundleSizes of 4 or less. Please adjust your input")
            sys.exit()  #   ends the program

    def getdsl(self):
        return self.dsl

    def getdsc(self):
        return self.dsc

    def getBundleSize(self):
        return self.size

    def getBundleDistance(self):
        return self.bundleDistance

