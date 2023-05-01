from System import System
class FaultCalculations:

    # Step 1 - Determine faulted bus n, and pre-fault voltage V_f
    # Step 2 - Solve for I_012 using fault type and all V_012s
    # Step 3 - Calculate I_abc and V_abc using Symmetrical Component Transform matrix

    def __init__(self, system: System):
        self.system = system
        # pre-fault voltage
        self.V_f = None
        # number of the bus that has a fault. n = busN - 1 for python indexing purposes
        self.n = None
        # bus_name stores the name of the bus with a fault to easily access values of the bus through the dictionary
        self.bus_name = None

    # Find_fault will cycle through the buses of the network and determine which, if any, bus has a fault
    # Then it will set the pre-fault voltage V_f, and set the bus number that has the fault
    def find_fault(self):
        for key in self.system.buses:
            if self.system.buses[key].faulted == True:
                self.bus_name = key
                self.V_f = self.system.buses[key].vdf

