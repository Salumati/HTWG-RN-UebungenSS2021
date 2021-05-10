from threading import Lock
from time import time
from math import floor

class _Statistics:
    def __init__(self):
        self.startTime = time()
        self.lastServedCustomerLock = Lock()
        self.lastServedCustomer = ("", 0)
        self.servedCustomersLock = Lock()
        self.shoppingTimesK1 = []
        self.shoppingTimesK1Lock = Lock()
        self.shoppingTimesK2 = []
        self.shoppingTimesK2Lock = Lock()
        self.servedCustomers = []
        self.droppedCustomerLock = Lock()
        self.droppedCustomers = {
            "Eingang": [],
            "Bäcker": [],
            "Wurst": [],
            "Käse": [],
            "Kasse" : [],
            "Ausgang": []
        }

    def setLastServedCustomer(self, customerName):
        self.lastServedCustomerLock.acquire()
        self.lastServedCustomer = (customerName, floor(time() - self.startTime))
        self.lastServedCustomerLock.release()

    def addServedCustomer(self, customerName):
        self.servedCustomersLock.acquire()
        self.servedCustomers.append(customerName)
        self.servedCustomersLock.release()

    def addDroppedCustomer(self, station, customerName):
        self.droppedCustomerLock.acquire()
        self.droppedCustomers[station].append(customerName)
        self.droppedCustomerLock.release()

    def completelyServedCustomers(self):
        uniqueDropped = []
        for station in self.droppedCustomers:
            for customer in self.droppedCustomers[station]:
                if customer not in uniqueDropped:
                    uniqueDropped.append(customer)
        return len(self.servedCustomers) - len(uniqueDropped)

    def droppedCustomerPercentage(self, station):
        return floor(len(self.droppedCustomers[station]) / len(self.servedCustomers) * 100)

    def addShoppingTimeK1(self, time):
        self.shoppingTimesK1Lock.acquire()
        self.shoppingTimesK1.append(time)
        self.shoppingTimesK1Lock.release()
    
    def addShoppingTimeK2(self, time):
        self.shoppingTimesK2Lock.acquire()
        self.shoppingTimesK2.append(time)
        self.shoppingTimesK2Lock.release()

    def averageShoppingTimeK1(self):
        allTimes = 0
        for timeK1 in self.shoppingTimesK1:
            allTimes += timeK1
        return floor(allTimes / len(self.shoppingTimesK1))
    def averageShoppingTimeK2(self):
        allTimes = 0
        for timeK2 in self.shoppingTimesK2:
            allTimes += timeK2
        return floor(allTimes / len(self.shoppingTimesK2))

Statistics = _Statistics()