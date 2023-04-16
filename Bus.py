import cmath

class Bus:
    #Class Attribute
    busCount = 0
    slackCount = 0
    load_count = 0
    vc_count = 0
    def __init__(self, name): #where should I set the bus voltage
        self.index = Bus.busCount
        self.name = name
        self.type = None
        self.vk = None
        self.vdf = None
        self.delta1 = None
        self.pk = None
        self.qk = None
        Bus.busCount += 1
        self.type = type
        # self.getBusTypeCount()

    def getBusTypeCount(self):
        if self.type == "Slack":
            Bus.slackCount += 1
        elif self.type == "Load":
            Bus.load_count += 1
        elif self.type == "VC":
            Bus.vc_count += 1
        elif self.type == None:
            return
        else:
            exit("Incorrect Bus Input Values for " + self.name)

    def calc_vdf(self):
        vpu_df = pd.DataFrame()
        vpu_df.loc[self.bus1, self.bus1] = cmath.rect(self.bus1.vk, self.bus1.delta1)
        vpu_df.loc[self.bus1, self.bus2] = cmath.rect(self.bus1.vk, self.bus1.delta1) - cmath.rect(self.bus2.vk, self.bus2.delta1)
        vpu_df.loc[self.bus2, self.bus1] = cmath.rect(self.bus2.vk, self.bus2.delta1)
        vpu_df.loc[self.bus2, self.bus2] = cmath.rect(self.bus2.vk, self.bus2.delta1) - cmath.rect(self.bus1.vk, self.bus1.delta1)
        ##check to see if this saves y as a variable
        self.vdf = vpu_df








