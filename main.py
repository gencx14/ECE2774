from Ybus import Ybus
from Network import Network
from PowerFlow import PowerFlow

# building the network
network_obj = Network('network1')

# adding geometry
network_obj.add_geometry('geometry1', -19.5, 30, 0, 30, 19.5, 30)

# adding line data
network_obj.add_transmission_line_type('Partridge', 2, network_obj.geometries['geometry1'], 0.0217, 0.642, 1.5, 0.385)

# creating buses
network_obj.add_bus('bus1')
network_obj.add_bus('bus2')
network_obj.add_bus('bus3')
network_obj.add_bus('bus4')
network_obj.add_bus('bus5')
network_obj.add_bus('bus6')
network_obj.add_bus('bus7')

# creating transmission lines
network_obj.add_transmission_line('L1', 'bus1', 'bus2', 10, network_obj.line_data['Partridge'])
network_obj.add_transmission_line('L2', 'bus2', 'bus3', 25, network_obj.line_data['Partridge'])
network_obj.add_transmission_line('L3', 'bus3', 'bus5', 20, network_obj.line_data['Partridge'])
network_obj.add_transmission_line('L4', 'bus4', 'bus6', 20, network_obj.line_data['Partridge'])
network_obj.add_transmission_line('L5', 'bus5', 'bus6', 10, network_obj.line_data['Partridge'])
network_obj.add_transmission_line('L6', 'bus4', 'bus5', 35, network_obj.line_data['Partridge'])

# creating transformer types
network_obj.add_transformer_type('T1', 125, 230, 20, 0.085, 10)
network_obj.add_transformer_type('T2', 200, 230, 18, 0.105, 12)

# creating transformers
network_obj.add_transformer('T1', network_obj.transformer_data['T1'], 'bus1', 'bus2')
network_obj.add_transformer('T2', network_obj.transformer_data['T2'], 'bus6', 'bus7')

# creating Ybus object
ybus_obj = Ybus('ybus1', network_obj)
ybus_obj.fill_ybus_matrix()
# ybus_obj.print_ybus_matrix()

# setting bus types, and relevant parameters
network_obj.buses['bus1'].set_bus_type('slack')
network_obj.buses['bus2'].set_bus_type('load')
network_obj.buses['bus3'].set_bus_type('load')
network_obj.buses['bus4'].set_bus_type('load')
network_obj.buses['bus5'].set_bus_type('load')
network_obj.buses['bus6'].set_bus_type('load')
network_obj.buses['bus7'].set_bus_type('PV')


# temp work - testing power mismatch
PF1_obj = PowerFlow(ybus_obj)
PF1_obj.power_mismatch()
PF1_obj.temp_out()
