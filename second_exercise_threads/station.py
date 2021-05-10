import event
import event_queue
import time
from time import sleep
from threading import Event, Lock

"""
Requirements:
every station is a thread, they all start at the begin of the simulation and sleep until a customer wakes them up.
Serving a customer gets simulated by putting the station thread to sleep for the given time, 
    after it wakes up again it puts the customer to sleep as well
each station has a Arrive at Station event (arrEv), it gets activated if a customers enters the station.
to serve a customer a serve Event (servEv) gets activated, 
    which puts the customer to sleep (servEv.wait) until the station wakes him up again (servEv.set)
 
Once a customer got served, the next customer in the queue gets served.
If there are no more customers in the queue, the stations thread goes to sleep (arrEv.clear)

The queue and the arrEv need to be protected with locks.
"""

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
