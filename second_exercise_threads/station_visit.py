from stations import Stations
from time import sleep
from config import sleepFactor

class StationVisit:
    def __init__(self, station, arrivalTime, servings=0, maxWait=0):
        self._station = station
        self.arrivalTime = arrivalTime
        self.servings = servings
        self.maxWait = maxWait

    def station(self):
        return Stations[self._station]

    def queue(self, customerName, serveEv):
        self.station().queueCustomer(customerName, serveEv, self.servings)

    def shouldNotSkip(self):
        return self.maxWait == 0 or self.maxWait >= self.station().queuedCustomers()

    def arrive(self, customerName, serveEv):
        print(customerName, "arrived at", self.station().name)
        sleep(self.arrivalTime * sleepFactor)
        self.queue(customerName, serveEv)
        self.station().arrive()
        
