class Bus:

    #Keeps Track of Number of Busses
    count = 0

    def __init__(self, Bus: str):
        #Bus Name
        self.Bus: str = Bus

        #Bus Index
        self.index: int = Bus.count

        #Increase Bus Number when Bus is Added
        Bus.count = Bus.count + 1

        #Initialization
        self.Delta = 0.0
        self.V = 0.0
        self.P = 0.0
        self.Q = 0.0

    def setBusType(self, BusType: str, Real: float, Imag: float):
        #Slack Bus
        if BusType == "Slack":
            self.BusType = "Slack"
            #Reference Voltage V = 1.0 pu and Delta = 0 degrees
            self.V = 1.0

        #Load Bus
        elif BusType == "Load":
            self.BusType = "Load"
            self.P = Real
            self.Q = Imag

        #Voltage Controlled Bus
        elif BusType == "Voltage Controlled":
            self.BusType = "Voltage Controlled"
            self.V = Imag
            self.P = Real

        #Check for Valid Bus Type
        else:
            print("Invalid Bus Type.")