from System import System
from Solution import Solution
from DisplayResults import DisplayResults
import Constants


system = System("system", 100e6, 230e3)
system.add_geometry("geometry1", -19.5, 30, 0, 30, 19.5, 30)
system.add_conductor("partridge", 0.642, 0.0217, 0.385, 460)
system.add_bundle("main", 2, 1.5, system.conductors["partridge"])
system.add_transmissionLineData("mainLine", system.bundles["main"], system.geometries["geometry1"], system.conductors["partridge"])
system.add_transmissionLine("L1", "bus2", "bus4", system.transmissionlineDataItems["mainLine"], 10)
system.add_transmissionLine("L2", "bus2", "bus3", system.transmissionlineDataItems["mainLine"], 25)
system.add_transmissionLine("L3", "bus3", "bus5", system.transmissionlineDataItems["mainLine"], 20)
system.add_transmissionLine("L4", "bus4", "bus6", system.transmissionlineDataItems["mainLine"], 20)
system.add_transmissionLine("L5", "bus5", "bus6", system.transmissionlineDataItems["mainLine"], 10)
system.add_transmissionLine("L6", "bus4", "bus5", system.transmissionlineDataItems["mainLine"], 35)
system.add_transformerData("Tx1data", 125000000, 20000, 230000, 0.085, 10,'D-Y', 0, 1)
system.add_transformerData("Tx2data", 200000000, 18000, 230000, 0.105, 12,'D-Y', 0, Constants.INF)
system.add_transformer("Tx1", "bus1", "bus2", system.transformerdataItems["Tx1data"])
system.add_transformer("Tx2", "bus6", "bus7", system.transformerdataItems["Tx2data"])
system.add_generator("G1", 1.0, 'bus1', 0.12, 0.14, 0.05, 0)
system.add_generator("G2", 1.0, 'bus7', 0.12, 0.14, 0.05, 1)
system.set_bus("bus1", "Slack", 1.0, 0.0)
system.set_bus("bus2", "Load", None, None, 0, 0)
system.set_bus("bus3", "Load", None, None, -110, -50)
system.set_bus("bus4", "Load", None, None, -100, -70)
system.set_bus("bus5", "Load", None, None, -100, -65)
system.set_bus("bus6", "Load", None, None, 0, 0)
system.set_bus("bus7", "VC", 1.0, 0, 200, 0)



# soln = Solution(system)
DisplayResults(system, Solution(system))
print()
