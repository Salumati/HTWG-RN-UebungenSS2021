from stations import Stations

class StationVisit:
    def __init__(self, station, arrivalTime, servings=0, maxWait=0):
        self._station = station
        self.arrivalTime = arrivalTime
        self.servings = servings
        self.maxWait = maxWait


    def servingTime(self):
        return self.servings * self.station().servingTime

    def copy(self):
        return StationVisit(self.station, self.arrivalTime, self.servings, self.maxWait)

    def station(self):
        return Stations[self._station]

    def queue(self, customerName):
        self.station().queueCustomer(customerName, self.servings)

    def stationIsNotEmpty(self):
        return self.station().isNotEmpty()

    def unqueue(self, customerName):
        self.station().unqueueCustomer(customerName)

    def shouldNotSkip(self):
        return self.maxWait == 0 or self.maxWait >= len(self.station().queuedCustomers())

    def queuedServingTime(self):
        return self.station().queuedCustomersServingTime()
