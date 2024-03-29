import math

import numpy as np
from Generator import Generator
from System import System
from TransmissionLine import TransmissionLine
from VoltageMatrix import VoltageMatrix
import cmath


class PowerFlow:
    def __init__(self, ybus, system: System):
        self.N = len(system.buses)
        self.tolerance = 0.0001
        self.system = system
        self.ybus = ybus
        self.plength = None
        self.qlength = None
        self.vlength = None
        self.delta_length = None
        self.y =None
        self.x = None
        self.dx = None
        self.dy = None
        self.f_x = None
        self.p_x = None
        self.q_x = None
        self.delta_y = None
        self.delta_x = None
        self.delta_p = None
        self.delta_q = None
        self.J1 = None
        self.J2 = None
        self.J3 = None
        self.J4 = None
        self.Jacob = None
        self.busarr = None
        self.ybusarr = None
        self.xbusarr = None
        self.tiebusses = None
        self.step1_y_array()
        self.step2_x_array_flatstart()
        self.Newton_Raphson()
        self.updateBusses()
        self.getvalues()
        #self.calcCurrent()
        #self.calcpower()
        #self.calc_power_loss()
        #  fill y for power equation from bus information

    #finds the y... THIS WORKS AS EXPECTED
    def step1_y_array(self):
        # find y array which contains starting power values but make sure that you are using the bus objects
        # 1. create a vertical array of zeros for our P values
        # Ptemp = np.zeros((len(self.system.buses) - Bus.slackCount, 1))   ***REMOVED OFF REC FROM PAOLO
        Ptemp = np.zeros((self.N, 1), dtype=float)
        # 2.  create a vertical array of zeros for our P values
        # Qtemp = np.zeros((len(self.system.buses) - Bus.slackCount, 1))    *** Removed off rec from Paolo
        Qtemp = np.zeros((self.N, 1), dtype=float)
        # 3. create an array of the buses objects except the ones that are voltage controlled and create the P&Q arrays
        i = 0
        self.busarr = np.zeros(self.N, dtype=object)
        for bus in self.system.buses:
            # if self.system.buses[bus].type == "Slack":            *** REMOVED OFF REC FROM PAOLO
              #  continue
            # busarr was added to be sure that we are editing the correct bus in final calculations
            self.busarr[i] = self.system.buses[bus]
            Ptemp[i] = self.system.buses[bus].pk
            Qtemp[i] = self.system.buses[bus].qk
            i += 1
        #trim excess storage from the matrix
        self.ybusarr = np.trim_zeros(self.busarr)
        self.plength = len(Ptemp)
        self.qlength = len(Qtemp)


        # 3. concatenate the arrays
        ytemp = np.zeros((self.plength + self.qlength, 1), dtype=float)
        ytemp = np.concatenate((Ptemp, Qtemp))

        self.y = ytemp


    # finds the x
    def step2_x_array_flatstart(self):
        #  find x array which contains flat start voltage and
        # 1. create a vertical array of zeros for our delta values (voltage angles), flat start phase angle = 0 degrees
        delta_temp = np.zeros((self.N, 1), dtype=float)
        # 2. create a vertical array of ones for our voltage magnitude values for our flat start (mag = 1.0 for all)
        volt_temp = np.zeros((self.N, 1), dtype=float)
        busarr = np.zeros(self.N, dtype=object)
        i = 0
        #  find slack voltages (will almost always be 1.0 and 0 degrees)
        '''
        for bus in self.system.buses:
            if self.system.buses[bus].type == "Slack":
                slackvoltage = self.system.buses[bus].vk
                slackdelta = self.system.buses[bus].delta1
                break
        '''

        # fill voltage and deltas array
        for bus in self.system.buses:
            if self.system.buses[bus].type == "Slack":
                volt_temp[i] = self.system.buses[bus].vk
                delta_temp[i] = self.system.buses[bus].delta1
                # continue - edit encouraged by Paulo
            elif self.system.buses[bus].type == "VC": # type 2 on paulos code
                volt_temp[i] = self.system.buses[bus].vk # v is assigned voltage by voltage control
                delta_temp[i] = 0.0
            else:
                volt_temp[i] = 1.0
                delta_temp[i] = 0.0
            busarr[i] = self.system.buses[bus]
            i += 1

        self.vlength = len(volt_temp)
        self.delta_length = len(volt_temp)

        self.xbusarr = np.trim_zeros(busarr)
        # 3. concatenate the arrays
        self.x = np.zeros((len(delta_temp) + len(volt_temp), 1), dtype=float)
        self.x = np.concatenate((delta_temp, volt_temp))

    def step3_find_fx(self):
        # self.N = len(self.system.buses)
        self.p_x = np.zeros(self.N, dtype=float)
        self.q_x = np.zeros(self.N, dtype=float)
        for k in range(self.N):
            for n in range(self.N):
                # Compute active power flow
                self.p_x[k] += self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.cos(
                    self.x[k] - self.x[n] - np.angle(self.ybus[k][n]))

                # Compute reactive power flow
                self.q_x[k] += self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(
                    self.x[k] - self.x[n] - np.angle(self.ybus[k][n]))
        self.f_x = np.concatenate((self.p_x, self.q_x))

    # returns the change in power
    def step4_find_delta_y(self):
        self.delta_p = np.zeros((len(self.p_x), 1), dtype=float)
        self.delta_y = np.zeros((len(self.f_x), 1), dtype=float)
        self.delta_q = np.zeros((len(self.q_x), 1), dtype=float)
        for k in range(len(self.f_x)):
            self.delta_y[k] = self.y[k] - self.f_x[k]
        for k in range(len(self.p_x)):
            self.delta_p[k] = self.y[k] - self.p_x[k]
        for k in range(len(self.q_x)):
            self.delta_q[k] = self.y[k + self.plength] - self.q_x[k]


    def calc_J1(self):
        self.J1 = np.zeros((self.plength, self.plength), dtype=float)
        for k in range(self.plength):
            for n in range(self.plength):
                if k != n:
                    self.J1[k][n] = self.x[k+self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin((self.x[k]) - (self.x[n]) - np.angle(self.ybus[k][n]))
                else:
                    temp = 0
                    for i in range(self.plength):
                        if i != n:
                            temp += abs(self.ybus[k][i]) * self.x[i+self.plength] * np.sin((self.x[k]) - (self.x[i]) - np.angle(self.ybus[k][i]))
                    self.J1[k][n] = -1 * self.x[k+self.plength] * temp

    def calc_J2(self):
        self.J2 = np.zeros((self.plength, self.plength), dtype=float)
        for k in range(self.plength):
            for n in range(self.plength):
                if k != n:
                    self.J2[k][n] = self.x[k+self.plength] * abs(self.ybus[k][n]) * np.cos((self.x[k]) - (self.x[n]) - np.angle(self.ybus[k][n]))
                else:
                    temp = 0
                    for i in range(self.plength):
                        temp += self.x[i + self.plength] * abs(self.ybus[k][i]) * np.cos((self.x[k]) - (self.x[i]) - np.angle(self.ybus[k][i]))
                    self.J2[k][n] = self.x[k + self.plength] * abs(self.ybus[k][n]) * np.cos(np.angle(self.ybus[k][n])) + temp

    def calc_J3(self):
        self.J3 = np.zeros((self.plength, self.plength), dtype=float)
        for k in range(self.plength):
            for n in range(self.plength):
                if k != n:
                    self.J3[k][n] = -1 * self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.cos(
                        (self.x[k]) - (self.x[n]) - np.angle(self.ybus[k][n]))
                else:
                    temp = 0
                    for i in range(self.plength):
                        if i != n:
                            temp += abs(self.ybus[k][i]) * self.x[i + self.plength] * np.cos(
                                (self.x[k]) - (self.x[i]) - np.angle(self.ybus[k][i]))
                    self.J3[k][n] = self.x[k + self.plength] * temp

    def calc_J4(self):
        self.J4 = np.zeros((self.plength, self.plength), dtype=float)
        for k in range(self.plength):
            for n in range(self.plength):
                if k != n:
                    self.J4[k][n] = self.x[k+self.plength] * abs(self.ybus[k][n]) * np.sin((self.x[k]) - (self.x[n]) - np.angle(self.ybus[k][n]))
                else:
                    temp = 0
                    for i in range(self.plength):
                        temp += self.x[i + self.plength] * abs(self.ybus[k][i]) * np.sin((self.x[k]) - (self.x[i]) - np.angle(self.ybus[k][i]))
                    self.J4[k][n] = (-1 * self.x[k + self.plength] * abs(self.ybus[k][n])) * np.sin(np.angle(self.ybus[k][n])) + temp

    def form_jacobian(self):
        self.calc_J1()
        self.calc_J2()
        self.calc_J3()
        self.calc_J4()
        self.Jacob = np.block([[self.J1, self.J2], [self.J3, self.J4]])

    def solveMismatch(self):
        count = 0
        self.N = int(self.Jacob.shape[0] / 2)
        dx = np.zeros(2 * self.N, dtype=float)
        dy = np.zeros(2 * self.N, dtype=float)

        tiebusses = np.zeros(2 * len(self.system.buses), dtype=object)
        self.tiebusses = np.zeros(2 * len(self.system.buses), dtype=object)
        n = 0
        for bus in self.system.buses:
            tiebusses[n] = self.system.buses[bus]
            tiebusses[n+len(self.system.buses)] = self.system.buses[bus]
            n+=1

        for n in range(self.N - 1, -1, -1): #iterate in reverse order
            if self.busarr[n].type == "Slack":
                self.Jacob = np.delete(arr=self.Jacob, obj=n + self.N, axis = 0)
                self.Jacob = np.delete(arr=self.Jacob, obj=n + self.N, axis = 1)
                self.Jacob = np.delete(arr=self.Jacob, obj=n, axis = 0)
                self.Jacob = np.delete(arr=self.Jacob, obj=n, axis = 1)
                self.delta_y = np.delete(arr=self.delta_y, obj = n + self.N)
                self.delta_y = np.delete(arr = self.delta_y, obj = n)
                tiebusses = np.delete(arr=tiebusses, obj=n+self.N)
                tiebusses = np.delete(arr=tiebusses, obj=n)
            elif self.busarr[n].type == "VC":       # delete the Q values
                count = count + 1
                self.Jacob = np.delete(arr=self.Jacob, obj=n + self.N, axis = 0)
                self.Jacob = np.delete(arr=self.Jacob, obj=n + self.N, axis = 1)
                self.delta_y = np.delete(arr=self.delta_y, obj=n+self.N)
                tiebusses = np.delete(arr=tiebusses, obj=n+self.N)
        self.tiebusses = tiebusses


        self.delta_x = np.dot(np.linalg.inv(self.Jacob), self.delta_y)
        #self.x = self.x + self.delta_x


        m_p = 0
        m_q = 0

        for n in range(self.N):
            if self.busarr[n].type == "Slack":
                continue
            elif self.busarr[n].type == "Load":
                dx[n] = self.delta_x[m_p]
                dx[n+self.N] = self.delta_x[self.N - 1 + m_q]
                dy[n] = self.delta_y[m_p]
                dy[n+self.N] = self.delta_y[self.N - 1 + m_q]
                m_p = m_p + 1
                m_q = m_q + 1
            elif self.busarr[n].type == "VC":
                dx[n] = self.delta_x[m_p]
                dy[n] = self.delta_y[m_p] # dont need
                m_p = m_p + 1
            # dx = np.trim_zeros(dx)
            # dy = np.trim_zeros(dy)
            dx = np.reshape(dx, (len(dx), 1))
        self.x = self.x + dx

    def updateBusses(self):
        for n in range(self.N):
            self.busarr[n].delta1 = float(self.x[n])
            self.busarr[n].vk = float(self.x[n + self.N])
            self.busarr[n].pk = float(self.y[n])
            self.busarr[n].qk = float(self.y[n + self.N])

    def Newton_Raphson(self):
        # 1. Set up y array for original P and Q values of all busses... not not in loop

        # 1. Set up y array based on inputs
        # 2. Set up flat start, set self.x voltage values and delta values to 1.o and 0.0, respectivly.. not in loop
        # 3. calculate power (find fx)
        self.N = len(self.system.buses)
        self.step3_find_fx()
        # 4. find delta y (y - fx) Power mismatch--> gives tolerance to know when we are complete
        self.step4_find_delta_y()
        # end the recursive function if tolerance is solved for
        #if np.amax(abs(self.delta_y)) < self.tolerance:
            # self.x = self.x + self.delta_x
           # print(self.printme)
           # return
        # form the jacobian
        self.form_jacobian()
        #solve the mismatch
        self.solveMismatch()
        if np.amax(abs(self.delta_y)) < self.tolerance:
            # self.x = self.x + self.delta_x
            return
        return self.Newton_Raphson()

    def getvalues(self):
        self.system.Plosses = np.zeros(len(self.system.y_elements), dtype=complex)
        i = 0
        slackS = 0
        for element_name, element in self.system.y_elements.items():
            if isinstance(element, Generator):
                continue
            # for row in element.buses:
            #  for col in element.buses:
            # index_row = self.system.buses[row].index
            # index_col = self.system.buses[col].index
            self.system.y_elements[element_name].voltDrop = (cmath.rect(self.system.buses[element.buses[0]].vk, self.system.buses[element.buses[0]].delta1) - cmath.rect(self.system.buses[element.buses[1]].vk, self.system.buses[element.buses[1]].delta1))
            self.system.y_elements[element_name].lineCurrent = (1 / element.zPu) * element.voltDrop
            self.system.y_elements[element_name].powerLosses = abs(element.lineCurrent) ** 2 * element.zPu
            self.system.y_elements[element_name].powerSending_S = self.system.buses[element.buses[0]].vk * element.lineCurrent.conjugate()
            self.system.y_elements[element_name].powerRecieving_S = self.system.buses[element.buses[1]].vk * element.lineCurrent.conjugate()
            self.system.Plosses[i] = element.powerLosses
            typebus1 = self.system.buses[element.buses[0]].type
            typebus2 = self.system.buses[element.buses[1]].type

            # find slack P and Q
            if typebus1 == "Slack":
                slackS += element.lineCurrent.conjugate() * self.system.buses[element.buses[0]].vk
                self.system.buses[element.buses[0]].pk = np.real(slackS)
                self.system.buses[element.buses[0]].qk = np.imag(slackS)
            # I am wondering if this should actually be -= instead of +=
            elif typebus2 == "Slack":
                slackS += element.lineCurrent.conjugate() * self.system.buses[element.buses[1]].vk
                self.system.buses[element.buses[1]].pk = np.real(slackS)
                self.system.buses[element.buses[1]].qk = np.imag(slackS)
            # find PV bus delta and Q
            elif typebus1 == "VC":
                #P = sqrt(3) V I cos delta
                delta = np.arccos(self.system.buses[element.buses[0]].pk / (self.system.buses[element.buses[0]].vk * abs(element.lineCurrent)))
                q = self.system.buses[element.buses[0]].vk * abs(element.lineCurrent) * np.sin(delta)
                self.system.buses[element.buses[0]].delta1 = delta
                self.system.buses[element.buses[0]].qk = q
            elif typebus2 == "VC":
                #P = sqrt(3) V I cos delta
                delta = np.arccos(self.system.buses[element.buses[1]].pk / (self.system.buses[element.buses[1]].vk * abs(element.lineCurrent)))
                q = self.system.buses[element.buses[1]].vk * abs(element.lineCurrent) * np.sin(delta)
                self.system.buses[element.buses[1]].delta1 = delta
                self.system.buses[element.buses[1]].qk = q
        # check ampacity if the current is more than the line is rated for turn currentOverRating to True else turn it to false
            if isinstance(element, TransmissionLine):
                currentRating = element.data.conductor.ampacity * self.system.bundles['main'].size / self.system.bases.ibase
                if float(abs(currentRating)) < (float(abs(element.lineCurrent))):
                    self.system.y_elements[element_name].currentOverRating = True
                else:
                    self.system.y_elements[element_name].currentOverRating = False

            i = i + 1
        self.system.totalPloss = np.sum(self.system.Plosses)


