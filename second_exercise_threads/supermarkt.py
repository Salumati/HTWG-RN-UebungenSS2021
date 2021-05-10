from customer import Customer
from stations import Stations, StartStations, StopStations
from station_visits import stationVisitsK1, stationVisitsK2
from statistics import Statistics
from customer_generator import CustomerGenerator
from time import sleep
from threading import Event, active_count, current_thread
from config import sleepFactor, terminationTime


"""
Requirements:
Real-time simulation: if a customer waits for 2 Minutes at a bakery, two actual Minutes pass in the simulation.
-> create a constant that reduces the actual wait time for testing purposes.

At the beginning:
create all station threads and put them to sleep
create customer threads and put them to sleep

simulation end:
when all start- and customer-threads are closed.
"""

# in seconds
customerK1StartTime = 0
customerK1SpawnTime = 200
customerK2StartTime = 1
customerK2SpawnTime = 60

class Supermarket:
    def __init__(self):
        self.stopEv = Event()
        
        self.customerK1 = Customer(
            "K1-1", stationVisitsK1
        )

        self.customerK2 = Customer(
            "K2-1", stationVisitsK2
        )

        self.customerGeneratorK1 = CustomerGenerator(self.customerK1.name, self.customerK1.stationVisits, customerK1SpawnTime, self.stopEv)
        self.customerGeneratorK2 = CustomerGenerator(self.customerK2.name, self.customerK2.stationVisits, customerK2SpawnTime, self.stopEv)

    def run(self):
        StartStations()
        sleep(customerK1StartTime * sleepFactor)
        print("first customer spawned")
        self.customerK1.start()
        self.customerGeneratorK1.start()
        sleep(customerK2StartTime * sleepFactor)
        print("second customer spawned")
        self.customerK2.start()
        self.customerGeneratorK2.start()

        sleep(terminationTime * sleepFactor)
        print("""
        ---------------------------
        stop spawning new customers
        ---------------------------
        """)
        self.stopEv.set()

        while(True):
            if(active_count() - 1 == len(Stations)):
                print("stopping stations")
                StopStations()
                break

        print("Last served customer", Statistics.lastServedCustomer[0], "at", Statistics.lastServedCustomer[1])
        print("Average shopping time for customer type 1", Statistics.averageShoppingTimeK1())
        print("Average shopping time for customer type 2", Statistics.averageShoppingTimeK2())
        print("Completely served customers", Statistics.completelyServedCustomers())
        for station in Stations:
            print("dropped customer percentage at station", station, ":", Statistics.droppedCustomerPercentage(station))

supermarket = Supermarket()
supermarket.run()
