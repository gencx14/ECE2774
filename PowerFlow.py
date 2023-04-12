import numpy as np

from System import System
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
        self.busarr = None
        self.ybusarr = None
        self.xbusarr = None
        self.printme = 0
        self.step1_y_array()
        self.step2_x_array_flatstart()
        self.Newton_Raphson()
        print()
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


        self.delta_x = np.dot(np.linalg.inv(self.Jacob), self.delta_y)
        #self.x = self.x + self.delta_x

        # I am not sure what this part does, and need to speak with Paolo about it
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

    def Newton_Raphson(self):
        # 1. Set up y array for original P and Q values of all busses... not not in loop

        print(self.printme)
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
            print(self.printme)
            return
        self.printme += 1
        return self.Newton_Raphson()







'''
    def calc_J1(self):
        for k in range(self.plength):
            for n in range(self.plength):
                if k == n:
                    self.J1[k][n] = -1 * (self.q_x[k] - (self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(np.deg2rad(self.x[k]) - np.deg2rad(self.x[n]) - cmath.phase(self.ybus[k][n]))))
                else:
                    self.J1[k][n] = self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(
                        np.deg2rad(self.x[k]) - np.deg2rad(self.x[n]) - cmath.phase(self.ybus[k][n]))
              
    def calc_J1(self):
        self.J1 = np.zeros((self.plength, self.plength))
        for k in range(self.plength):
            for n in range(self.plength):
                if k != n:
                    self.J1[k][n] = self.x[k+sekf.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(np.deg2rad(self.x[k]) * np.deg2rad(self.x[n])* cmath.phase(self.ybus[k][n]))
                else:
                    temp = 0
                    for i in range(self.plength):
                        if i != n:
                            temp += abs(self.ybus[k][i]) * self.x[i+self.plength] * np.sin(np.deg2rad(self.x[k]) - np.deg2rad(self.x[i]) - cmath.phase(self.ybus[k][i]))
                    self.J1[k][n] = self.x[k+self.plength] * temp
                    
                        
                    


    # find the jacobian
    def find_jacob(self):
            for row in element.buses:
                for col in element.buses:
                    index_row = self.system.buses[row].index
                    index_col = self.system.buses[col].index

                    self.J1[index_row, index_col] = self.p_x[index_row, 1] * self.system.ybus[index_row, index_col]

    def calc_J1(self):
        for k in range(self.plength):
            for n in range(self.plength):
                if k == n:
                    self.J1[k][n] = -1 * (self.q_x[k] - (self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(np.deg2rad(self.x[k]) - np.deg2rad(self.x[n]) - cmath.phase(self.ybus[k][n]))))
                else:
                    self.J1[k][n] = self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(
                        np.deg2rad(self.x[k]) - np.deg2rad(self.x[n]) - cmath.phase(self.ybus[k][n]))


    def calc_J2(self):
        temp = 0
        for k in range(self.plength):
            for n in range(self.plength):
                t
                if k == n:
                    self.J2[k][n] = self.x[k + self.plength] * abs(self.ybus[k][n]) * cmath.cos(cmath.phase(self.ybus[k][n]))






         J1_df = pd.DataFrame()
        J1_df.loc[self.ybusarr[k].index, self.ybusarr[k].index] =
        J1_df.loc[self.ybusarr[k].index, self.ybusarr[n].index] = self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.sin(np.rad2deg(self.x[k]) - np.rad2deg(self.x[n]) - np.rad2deg(cmath.phase(self.ybus[k][n])))
        J1_df.loc[self.ybusarr[n].index, self.ybusarr[k].index] = self.x[n + self.plength] * abs(self.ybus[n][k]) * self.x[k + self.plength] * np.sin(np.rad2deg(self.x[n]) - np.rad2deg(self.x[k]) - np.rad2deg(cmath.phase(self.ybus[n][k])))
        J1_df.loc[self.ybusarr[n], self.ybusarr[n]] =
        ##check to see if this saves y as a variable
        self.J1 = J1_df 

    def calc_J2(self, k, n):
        J2_df = pd.DataFrame()
        J2_df.loc[self.ybusarr[k].index, self.ybusarr[k].index] =
        J2_df.loc[self.ybusarr[k].index, self.ybusarr[n].index] = self.x[k + self.plength] * abs(self.ybus[k][n]) * np.cos(np.rad2deg(self.x[k]) - np.rad2deg(self.x[n]) - np.rad2deg(cmath.phase(self.ybus[k][n])))
        J2_df.loc[self.ybusarr[n].index, self.ybusarr[k].index] = self.x[n + self.plength] * abs(self.ybus[n][k]) * np.cos(np.rad2deg(self.x[n]) - np.rad2deg(self.x[k]) - np.rad2deg(cmath.phase(self.ybus[n][k])))
        J2_df.loc[self.ybusarr[n], self.ybusarr[n]] =
        ##check to see if this saves y as a variable
        self.J2 = J2_df

    def calc_J3(self, k, n):
        J3_df = pd.DataFrame()
        J3_df.loc[self.ybusarr[k].index, self.ybusarr[n].index] =
        J3_df.loc[self.ybusarr[k].index, self.ybusarr[k].index] = -1 * self.x[k + self.plength] * abs(self.ybus[k][n]) * self.x[n + self.plength] * np.cos(np.rad2deg(self.x[k]) - np.rad2deg(self.x[n]) - np.rad2deg(cmath.phase(self.ybus[k][n])))
        J3_df.loc[self.ybusarr[n].index, self.ybusarr[k].index] = -1 * self.x[n + self.plength] * abs(self.ybus[n][k]) * self.x[k + self.plength] * np.sin(np.rad2deg(self.x[n]) - np.rad2deg(self.x[k]) - np.rad2deg(cmath.phase(self.ybus[n][k])))
        J3_df.loc[self.ybusarr[n], self.ybusarr[n]] =
        ##check to see if this saves y as a variable
        self.J3 = J3_df

    def calc_J4(self, k, n):                    #IF THIS ISNT WORKING CHECK YOUR USE OF rad2deg function... should prob only be on outside!
        J4_df = pd.DataFrame()
        J4_df.loc[self.ybusarr[k].index, self.ybusarr[k].index] =
        J4_df.loc[self.ybusarr[k].index, self.ybusarr[n].index] = self.x[k + self.plength] * abs(self.ybus[k][n]) * np.sin(np.rad2deg(self.x[k]) - np.rad2deg(self.x[n]) - np.rad2deg(cmath.phase(self.ybus[k][n])))
        J4_df.loc[self.ybusarr[n].index, self.ybusarr[k].index] = self.x[n + self.plength] * abs(self.ybus[n][k]) * np.sin(np.rad2deg(self.x[n]) - np.rad2deg(self.x[k]) - np.rad2deg(cmath.phase(self.ybus[n][k])))
        J4_df.loc[self.ybusarr[n], self.ybusarr[n]] =
        ##check to see if this saves y as a variable
        self.J4 = J4_df





        # vector of every P, Q

        #find pk = p - px
'''
