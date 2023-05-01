from System import System
class FaultCalculations:

    # Step 1 - Determine faulted bus n, and pre-fault voltage V_f
    # Step 2 - Solve for I_012 using fault type and all V_012s
    # Step 3 - Calculate I_abc and V_abc using Symmetrical Component Transform matrix

    def __init__(self, system: System):
        self.system = system
        # pre-fault voltage
        self.V_f = None
        # bus_name stores the name of the bus with a fault to easily access values of the bus through the dictionary
        self.bus_name = None
        # zero sequence current of faulted bus
        self.In_0 = None
        # positive sequence current of faulted bus
        self.In_1 = None
        # negative sequence current of faulted bus
        self.In_2 = None
        # zero sequence voltage of faulted bus
        self.Vn_0 = None
        # positive sequence voltage of faulted bus
        self.Vn_1 = None
        # negative sequence voltage of faulted bus
        self.Vn_2 = None

    # Find_fault will cycle through the buses of the network and determine which, if any, bus has a fault
    # Then it will set the pre-fault voltage V_f, and set the bus_name to the bus that has the fault
    def find_fault(self):
        for key in self.system.buses:
            if self.system.buses[key].faulted == True:
                self.bus_name = key
                self.V_f = complex(self.system.buses[key].vk, self.system.buses[key].delta1)
            else:
                print("No fault detected")

    # Solve for In_0, In_1, and In_2 for a Symmetrical Fault
    def symmetrical_fault(self):

    # Solve for In_0, In_1, and In_2 for a Single Line-to-Ground Fault
    def single_linetoground_fault(self):

    # Solve for In_0, In_1, and In_2 for a Line-to_Line Fault
    def linetoline_fault(self):

    # Solve for In_0, In_1, and In_2 for a Double Line-to-Ground Fault
    def double_linetoground_fault(self):

    # Solves for Vn_0, Vn_1, and Vn_2 for the faulted bus
    def sequence_voltage_solver(self):
        if self.system.buses[self.bus_name].fault_type == 0:
            self.symmetrical_fault()

        elif self.system.buses[self.bus_name].fault_type == 1:
            self.single_linetoground_fault()

        elif self.system.buses[self.bus_name].fault_type == 1:
            self.linetoline_fault()

        else:
            self.double_linetoground_fault()

        # Matrix multiplication of sequence current and impedances to solve for voltages


