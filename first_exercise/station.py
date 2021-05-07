import event
import event_queue
import time


class QueuedCustomer:
    def __init__(self, name, servings):
        self.name = name
        self.servings = servings
class Station:
    def __init__(self, name, servingTime=0):
        self.name = name
        self.servingTime = servingTime
        self.customerQueue = []

    def queueCustomer(self, customerName, servings):
        self.customerQueue.append(QueuedCustomer(customerName, servings))

    def unqueueCustomer(self, customerName):
        self.customerQueue.pop()

    def queuedCustomers(self):
        return self.customerQueue

    def isNotEmpty(self):
        return len(self.queuedCustomers()) > 0

    def copy(self):
        return Station(self.name, self.servingTime)

    def queuedCustomersServingTime(self):
        time = 0
        for queuedCustomer in self.customerQueue:
            time += queuedCustomer.servings * self.servingTime
        return time
