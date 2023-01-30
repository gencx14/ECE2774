from Circuit import Circuit
from Solution import Solution
circuitObject = Circuit('myCircuit')
circuitObject.addResistorElement('Rab', 'A', 'B', 5)
circuitObject.addLoadElement('Lb', 'B', 2000.0, 100.0)
circuitObject.addVsourceElement('Va', 'A', 100.0)

solution_obj = Solution(circuitObject)
solution_obj.do_power_flow()
solution_obj.print_nodal_voltages()

print("Nick said this line should be deleted because it is just a test.")






