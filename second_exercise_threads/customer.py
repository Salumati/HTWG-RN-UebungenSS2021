from threading import Thread, Event
from statistics import Statistics
from time import time

"""
Requirements:
every Customer is a Thread, they start at the begin of the simulation.
Time between Station is simulated by putting the customer to sleep.
If the customer enters a station they get put into the station queue. 

We have one start-thread per customer type, which gets send to sleep after creating a customer,
"""

class Customer(Thread):
    def __init__(self, name, stationVisits):
        Thread.__init__(self)
        self.name = name
        self.stationVisits = stationVisits
        self.serveEv = Event()
        self.startTime = 0

    def run(self):
        self.startTime = time()
        self.arriveStation(0)

    def arriveStation(self, stationId):
        self.serveEv.clear()
        
        if stationId == len(self.stationVisits):
            Statistics.setLastServedCustomer(self.name)
            Statistics.addServedCustomer(self.name)
            customerType = self.name.split("-")[0]
            if customerType == "K1":
                Statistics.addShoppingTimeK1(time() - self.startTime)
            elif customerType == "K2":
                Statistics.addShoppingTimeK2(time() - self.startTime)
            return

        stationVisit = self.stationVisits[stationId]
        
        if stationVisit.shouldNotSkip():
            stationVisit.arrive(self.name, self.serveEv)
            self.serveEv.wait()
        else:
            Statistics.addDroppedCustomer(stationVisit.station().name, self.name)

        self.arriveStation(stationId + 1)
        