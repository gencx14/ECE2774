from Solution import Solution
from System import System
import pandas as pd
from PowerFlow import PowerFlow

class DisplayResults:
    def __init__(self):
        # self.system = system
        # self.solution = solution
        print("This code was designed for ECE 2774 and ECE 1774 by Nicholas Genco, Lucas Villaba, and Cole Florey.\n"
              "The course is led by Dr. Robert Kerestes and Paolo Radatz at the Universit of Pittsburgh.\n"
              "\n"
              "The Objective: Design a 6-Node Looped Transmission System that is able to be expanded upon\n"
              "Milestones:\n"
              "\t   1. Develop Power Flow System Ybus Matrix\n"
              "\t   2. Produce Power Flow Input Data, Jacobian, and Injection Equations\n"
              "\t   3. Solve Power System Power Flow\n"
              "\t   4. Var Limits and Different Solvers (NOT DEVLOPED)\n"
              "\t   5. Sequence Networks\n"
              "\t   6. Fault Calculations (NOT DEVELOPED)\n"
              "\n"
              "Elements you can add:\n"
              "\t   1. Transmission Line\n"
              "\t\t     - Geometry\n"
              "\t\t     - Conductor\n"
              "\t\t     - Bundle\n"
              "\t\t\t       ** Subelements must be added prior to Transmission Lines and must be added in order of appearance\n"
              "\t   2. Transformer\n"
              "\t   3. Bus\n"
              "\t   4. Generator\n\n")
        self.build_system()
        Ybus = pd.DataFrame(self.solution.ybus, columns=self.system.buses.keys())
        Ybus.index = self.system.buses.keys()
        Ybus1 = pd.DataFrame(self.solution.ybus1, columns = self.system.buses.keys())
        Ybus1.index = self.system.buses.keys()
        Ybus2 = pd.DataFrame(self.solution.ybus2, columns = self.system.buses.keys())
        Ybus2.index = self.system.buses.keys()
        Ybus0 = pd.DataFrame(self.solution.ybus0, columns = self.system.buses.keys())
        Ybus0.index = self.system.buses.keys()

    def build_system(self):
        systemname = input("Please name your system name\n")
        base
        system_list = system.split()
        system = System(system_list[0], float(system_list[1], float(system_list[2])))

        add = int(input("Which Element would you like to add first:\n"
                    "\t   1. Transmission Line\n"
                    "\t   2. Transformer\n"
                    "\t   3. Generator\n"
                    "\t   0. Finish\n"))
        if add < 0 or add > 3:
            print("INVALID SYSTEM ITEM SELECTED, Please input correct int value.\n")
            self.build_system()
        elif add == 0:
            self.setBusses()
            return
        elif add == 1:
            if len(self.system.transmissionlines) > 0:
                geom_string = ', '.join(list(self.system.geometries.keys()))
                tline_string = ', '.join(list(self.system.transmissionlines.keys()))
                cond_string = ', '.join(list(self.system.conductors.keys()))
                bund_string = ', '.join(list(self.system.bundles.keys()))
                print("Adding a transmission line:\n"
                      "\t   1. Select or Add a Geometry (if you choose a new name a new geometry will be created)\n"
                      f"\t\t     Current Geometries: {geom_string}\n")
                name = input("Enter Geometry Name: \n")
                if name not in self.system.geometries:
                    values = input(f"Please enter your {name} geometry configuration seperated by a space: \n"
                          "\tInput Key: ax ay bx by cx cy")
                    values_list = values.split()
                    values_list = float(values_list)
                    self.system.add_geometry(name, *values_list)
            else:
                print("Adding a transmission line:\n"
                      "\t   1. Add a Geometry\n")
                name = input("Enter Geometry Name: \n")
                values = input(f"Please enter your {name} geometry configuration seperated by a space: \n"
                                   "\tInput Key: ax, ay, bx, by, cx, cy")
                values_list = values.split()
                values_list = float(values_list)
                self.system.add_geometry(name, *values_list)




    def setBusses(self):
        print()







