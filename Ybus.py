import numpy as np
from Network import Network


class Ybus:

    def __init__(self, name, network: Network):
        self.network = network
        self.name = name
        self.Y_matrix = np.zeros((self.network.n, self.network.n))      # creates an n by n matrix of zeros where
        # n is the number of buses in the network

    def fill_ybus_matrix(self):         # fills values of Ybus matrix with necessary values
        self.Y_matrix[0][0] = str(self.network.transformers['T1'].y)
        self.Y_matrix[0][1] = - self.network.transformers['T1'].y
        self.Y_matrix[1][0] = self.Y_matrix[1][0]
        self.Y_matrix[1][1] = self.network.transformers['T1'].y + self.network.lines['L1'].y + self.network.lines['L2'].y
        self.Y_matrix[1][2] = - self.network.lines['L2'].y
        self.Y_matrix[1][3] = - self.network.lines['L1'].y
        self.Y_matrix[2][1] = self.Y_matrix[1][2]
        self.Y_matrix[2][2] = self.network.lines['L2'].y + self.network.lines['L3'].y
        self.Y_matrix[2][4] = - self.network.lines['L3'].y
        self.Y_matrix[3][1] = self.Y_matrix[1][3]
        self.Y_matrix[3][3] = (self.network.lines['L1'].y + self.network.lines['L4'].y + self.network.lines['L6'].y)
        self.Y_matrix[3][4] = - self.network.lines['L6'].y
        self.Y_matrix[3][5] = - self.network.lines['L4'].y
        self.Y_matrix[4][2] = self.Y_matrix[2][4]
        self.Y_matrix[4][3] = self.Y_matrix[3][4]
        self.Y_matrix[4][4] = self.network.lines['L3'].y + self.network.lines['L5'].y + self.network.lines['L6'].y
        self.Y_matrix[4][5] = - self.network.lines['L5'].y
        self.Y_matrix[5][3] = self.Y_matrix[3][5]
        self.Y_matrix[5][4] = self.Y_matrix[4][5]
        self.Y_matrix[5][5] = self.network.transformers['T2'].y + self.network.lines['L4'].y + self.network.lines['L5'].y
        self.Y_matrix[5][6] = - self.network.transformers['T2'].y
        self.Y_matrix[6][5] = self.Y_matrix[5][6]
        self.Y_matrix[6][6] = self.network.transformers['T2'].y

    def print_ybus_matrix(self):        # outputs the values in the Ybus matrix
        print(self.Y_matrix)
