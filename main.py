from Ybus import Ybus
from Network import Network

# building the network
network_obj = Network('network1')
network_obj.add_geometry('geometry1',-19.5, 30, 0, 30, 19.5, 30)
network_obj.add_transmission_line_type('Partridge', 2, network_obj.geometries['geometry1'], 0.0217, 0.642, 1.5, 0.385)
network_obj.add_bus('bus1')
network_obj.add_bus('bus2')
network_obj.add_bus('bus3')
network_obj.add_bus('bus4')
network_obj.add_bus('bus5')
network_obj.add_bus('bus6')
network_obj.add_bus('bus7')

network_obj.add_transmission_line('L1', bus1, bus2, )
