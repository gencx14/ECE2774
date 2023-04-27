from YBus import YBus
from Geometry import Geometry
from Bundles import Bundles
from ConductorData import ConductorData

#Building the Network
PartridgeData = ConductorData(0.2604, 0.321, 0.385)
BundledData = Bundles(2, PartridgeData, 18.0)
PhaseGeometry = Geometry(0, 0, 19.5, 0, 40, 0)

#Generate the Matrix
Matrix = YBus("Matrix")

#Adding Generators to Matrix
Matrix.addGenerator("G1", "B1", 100)
Matrix.addGenerator("G2", "B7", 100)

#Adding Transformers to Matrix
Matrix.addTransformer("T1", "B1", "B2", 125, 20, 230, 0.085, 10)
Matrix.addTransformer("T2", "B7", "B6", 200, 18, 230, 0.105, 12)

#Adding Transmission Lines to Matrix
Matrix.addTransmissionLine("L1", 10, PhaseGeometry, BundledData, "B2", "B4", 1.5)
Matrix.addTransmissionLine("L2", 25, PhaseGeometry, BundledData, "B2", "B3", 1.5)
Matrix.addTransmissionLine("L3", 20, PhaseGeometry, BundledData, "B3", "B5", 1.5)
Matrix.addTransmissionLine("L4", 20, PhaseGeometry, BundledData, "B4", "B6", 1.5)
Matrix.addTransmissionLine("L5", 10, PhaseGeometry, BundledData, "B5", "B6", 1.5)
Matrix.addTransmissionLine("L6", 35, PhaseGeometry, BundledData, "B4", "B5", 1.5)

#Setting Busses
Matrix.setBusType("B1", "Slack", 0, 0)
Matrix.setBusType("B2", "Load", 0, 0)
Matrix.setBusType("B3", "Load", 110, 50)
Matrix.setBusType("B4", "Load", 100, 70)
Matrix.setBusType("B5", "Load", 100, 65)
Matrix.setBusType("B6", "Load", 0, 0)
Matrix.setBusType("B7", "Voltage Controlled", 200, 1)

#Ybus Matrix
YBusMatrix = Matrix.calculate_YBus_Matrix()
Y_Bus_List = Matrix.Buses