from threading import Thread
from customer import Customer
from time import sleep
from config import sleepFactor

class CustomerGenerator(Thread):
    def __init__(self, name, stationVisits, spawnTime, stopEv):
        Thread.__init__(self)
        self.name = name
        self.stationVisits = stationVisits
        self.spawnTime = spawnTime
        self.stopEv = stopEv

    def run(self):
        while(True):
            if self.stopEv.is_set():
                break
            nameSplit = self.name.split("-")
            name = f"{nameSplit[0]}-{str(int(nameSplit[1])+1)}"
            self.name = name
            customer = Customer(self.name, self.stationVisits)
            sleep(self.spawnTime * sleepFactor)
            print("customer", self.name, "spawned")
            customer.start()