from time import sleep
from threading import Event, Lock, Thread
from config import sleepFactor

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
    def __init__(self, name, serveEv, servings):
        self.name = name
        self.servings = servings
        self.serveEv = serveEv

class Station(Thread):
    def __init__(self, name, stopEv, servingTime=0):
        Thread.__init__(self)
        self.name = name
        self.servingTime = servingTime
        self.customerQueue = []
        self.arrEv = Event()
        self.queueLock = Lock()
        self.arrEvLock = Lock()
        self.stopEv = stopEv
        
    
    def run(self):
        while(not self.stopEv.is_set()):
            self.arrEv.wait()
            if self.arrEv.is_set():
                while(self.queuedCustomers() > 0):
                    customer = self.unqueueCustomer()
                    sleep(customer.servings * self.servingTime * sleepFactor)
                    print("station", self.name, "served", customer.name)
                    customer.serveEv.set()
                self.arrEv.clear()

    


    def queuedCustomers(self):
        return len(self.customerQueue)

    def queueCustomer(self, customerName, serveEv, servings):
        self.queueLock.acquire()
        self.customerQueue.append(QueuedCustomer(customerName, serveEv, servings))
        self.queueLock.release()

    def arrive(self):
        self.arrEvLock.acquire()
        self.arrEv.set()
        self.arrEvLock.release()

    def unqueueCustomer(self):
        self.queueLock.acquire()
        customer = self.customerQueue.pop()
        self.queueLock.release()
        return customer
