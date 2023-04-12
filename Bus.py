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








