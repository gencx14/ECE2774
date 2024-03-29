from Solution import Solution
from System import System
from Generator import Generator
import pandas as pd
import numpy as np
import cmath
from PowerFlow import PowerFlow

class DisplayResults:
    def __init__(self, system: System, solution: Solution):
        self.system = system
        self.solution = solution
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
              "\t   4. Generator\n\n"
              "System is built with bus order being dictated by order of adding the bus to the system.\n"
              f"Your current bus order is {list(self.system.buses.keys())}\n\n")
        changebus = int(input("If you would like to reorder the buses before displaying results enter 1, otherwise enter 0: "))
        while changebus < 0 or changebus > 1 or not isinstance(changebus, int):
            changebus = int(input("Please enter 1 if you would like to reorder the bus display or 0 if you would not like to: "))


        # self.build_system() This function is used for the full user interfaces that guides the user to build their own system step by step
        Ybus = pd.DataFrame(self.solution.ybus, columns=self.system.buses.keys())
        Ybus.index = self.system.buses.keys()
        Ybus1 = pd.DataFrame(self.solution.ybus1, columns = self.system.buses.keys())
        Ybus1.index = self.system.buses.keys()
        Ybus2 = pd.DataFrame(self.solution.ybus2, columns = self.system.buses.keys())
        Ybus2.index = self.system.buses.keys()
        Ybus0 = pd.DataFrame(self.solution.ybus0, columns = self.system.buses.keys())
        Ybus0.index = self.system.buses.keys()
        Zbus = pd.DataFrame(self.solution.zbus, columns=self.system.buses.keys())
        Zbus.index = self.system.buses.keys()
        Zbus1 = pd.DataFrame(self.solution.zbus1, columns=self.system.buses.keys())
        Zbus1.index = self.system.buses.keys()
        Zbus2 = pd.DataFrame(self.solution.zbus2, columns=self.system.buses.keys())
        Zbus2.index = self.system.buses.keys()
        Zbus0 = pd.DataFrame(self.solution.zbus0, columns=self.system.buses.keys())
        Zbus0.index = self.system.buses.keys()
        pfbusarr = np.concatenate((np.array(list(self.system.buses.keys())), np.array(list(self.system.buses.keys()))))
        powerflow_X = pd.DataFrame(self.solution.pf.x, index=pfbusarr)
        powerflow_Y = pd.DataFrame(self.solution.pf.y, index=pfbusarr)
        JacobIndex = np.array([bus.name for bus in self.solution.pf.tiebusses])
        Jacobian = pd.DataFrame(self.solution.pf.Jacob, index=JacobIndex, columns=JacobIndex)
        print('NOTICE: JACOBIAN, Power Flow X and Y order is NOT RECONFIGURABLE and user should take attention to understand what value they are looking at\n')
        if changebus == 1:
            new_order = input("Enter the new order of the index separated by spaces: ").split()
            pfbussarr = new_order[:7] + new_order[:7]
            Ybus = Ybus.reindex(index=new_order, columns=new_order)
            Ybus1 = Ybus1.reindex(index=new_order, columns=new_order)
            Ybus2 = Ybus2.reindex(index=new_order, columns=new_order)
            Ybus0 = Ybus0.reindex(index=new_order, columns=new_order)
            Zbus = Zbus.reindex(index=new_order, columns=new_order)
            Zbus1 = Zbus1.reindex(index=new_order, columns=new_order)
            Zbus2 = Zbus2.reindex(index=new_order, columns=new_order)
            Zbus0 = Zbus0.reindex(index=new_order, columns=new_order)
            powerflow_X = powerflow_X.reindex(index=pfbusarr)
            powerflow_Y = powerflow_Y.reindex(index=pfbusarr)

        Ybus_formatted = Ybus.applymap(lambda c: f"({c.real:.3f} + {c.imag:.3f}j)")
        Ybus1_formatted = Ybus1.applymap(lambda c: f"({c.real:.3f} + {c.imag:.3f}j)")
        Ybus2_formatted = Ybus2.applymap(lambda c: f"({c.real:.3f} + {c.imag:.3f}j)")
        Ybus0_formatted = Ybus0.applymap(lambda c: f"({c.real:.3f} + {c.imag:.3f}j)")


        print(f"The has {len(self.system.y_elements)} elements and {len(self.system.buses)} busses.\n")
        for elementName,element in self.system.y_elements.items():
            if isinstance(element, Generator):
                print(f"The {elementName} information was not included\n")
                continue
            print(f" {elementName}, has the following values.\n"
                  f"\t  The Voltage drop across the {elementName} is {abs(self.system.y_elements[elementName].voltDrop) * self.system.bases.vbase}.\n"
                  f"\t  The Line Current is {abs(self.system.y_elements[elementName].lineCurrent) * self.system.bases.ibase} Amps. Is the system overcurrent: {element.currentOverRating}\n"
                  f"\t  The powerLosses in the line is {np.real(self.system.y_elements[elementName].powerLosses) * self.system.bases.pbase}. \n"
                  f"\t  The powerSending from {element.bus1} is {self.system.y_elements[elementName].powerSending_S * 3 * self.system.bases.pbase}.\n"
                  f"\t  The power being Recieved by {element.bus2} is {self.system.y_elements[elementName].powerSending_S * 3 * self.system.bases.pbase}.\n\n")



        print(f"Y Bus:\n {Ybus}\n\n"
              f"Ybus0:\n {Ybus0}\n\n"
              f"Ybus1:\n {Ybus1}\n\n"
              f"Ybus2:\n {Ybus2}\n\n"
              f"Z Bus:\n {Zbus}\n\n"
              f"Zbus0:\n {Zbus0}\n\n"
              f"Zbus1:\n {Zbus1}\n\n"
              f"Zbus2:\n {Zbus2}\n\n"
              f"X array [delta in rads, voltage]:\n {powerflow_X}\n\n"
              f"Y array [P in per unit, Q in per unit]:\n {powerflow_Y}\n\n"
              f"Jacobian:\n {Jacobian}\n\n")
        self.Ybus = Ybus
        self.Ybus0 = Ybus0
        self.Ybus1 = Ybus1
        self.Ybus2 = Ybus2
        self.Zbus = Zbus
        self.Zbus0 = Zbus0
        self.Zbus1 = Zbus1
        self.Zbus2 = Zbus2






'''
            new_Jacobindex = []
            for i in new_order:
                if i in Jacobian.index:
                    new_Jacobindex.append(i)
            Jacobian1 = Jacobian.iloc[:len(new_Jacobindex), :len(new_Jacobindex)]
            Jacobian1 = Jacobian.reindex(index=new_Jacobindex, columns=new_Jacobindex)
            halflength = len(new_Jacobindex)
            for i in new_order:
                if i in Jacobian.index[halflength:]:
                    new_Jacobindex.append(i + ' a')
            Jacobian = Jacobian.reindex(index=new_Jacobindex[halflength+1:len(new_Jacobindex)], columns=new_Jacobindex[halflength:len(new_Jacobindex)])
'''








'''
 User interface still in development
    def build_system(self):
        systemname = input("Please name your system name: \n")
        basepower = int(input("Please enter system base power (enter full number): \n"))
        basevoltage = int(input("Please enter system base voltage (enter full number): \n"))
        self.system = System(systemname, basepower, basevoltage)

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
                      "\t   2. Select or Add "
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
                values_list = [float(v) for v in values_list]
                self.system.add_geometry(name, *values_list)

'''









