from event_queue import EventQueue
from customer import Customer
from station_visits import stationVisitsK1, stationVisitsK2
from event_queue import EventQueue
from statistics import Statistics
from stations import Stations

# in seconds
customerK1StartTime = 0
customerK1SpawnTime = 20
customerK2StartTime = 1
customerK2SpawnTime = 60

class Supermarket:
    def __init__(self):
        self.customerK1 = Customer(
            "K1-1", stationVisitsK1, customerK1StartTime, customerK1SpawnTime
        )

        self.customerK2 = Customer(
            "K2-1", stationVisitsK2, customerK2StartTime, customerK2SpawnTime
        )

    def run(self):
        self.customerK1.startShopping()
        self.customerK2.startShopping()

        EventQueue.work()
        print(EventQueue)
        
        statistics = Statistics(EventQueue.history)
        print("Last served customer time", statistics.lastServedCustomerTime())
        print("Average complete shopping time", statistics.completeShoppingTime())
        print("Completely served customers", statistics.servedCustomers())
        
        for station in Stations:
            print("Dropped customer percentage for", station, statistics.droppedStationPercentage(station))

supermarket = Supermarket()
supermarket.run()
