from event import Event, EventType, StationEventArgs, SpawnCustomerEventArgs, QueueCustomerEventArgs
from config import spawnFactor, terminationTime
from event_queue import EventQueue


class Customer:
    def __init__(self, name, stationVisits, startTime, spawnTime):
        self.name = name
        self.stationVisits = stationVisits
        self.startTime = startTime
        self.spawnTime = spawnTime

    def startShopping(self):
        self.spawnNext()
        self.startEvent()

    def arriveStation(self, args):
        print(args.stationId, self.name)
        stationVisit = self.stationVisits[args.stationId]

        time = args.time + stationVisit.arrivalTime
        if stationVisit.shouldNotSkip():
            if stationVisit.stationIsNotEmpty():
                EventQueue.push(
                    Event(
                        EventType.QUEUE_CUSTOMER,
                        time,
                        2,
                        self.queue,
                        QueueCustomerEventArgs(args.stationId, time, self.name),
                    )
                )
            else:
                self.queue(QueueCustomerEventArgs(args.stationId, time, self.name))
        else:
            print("drop", args.stationId, self.name)
            self.dropStation(time, args.stationId)

        return

    def dropStation(self, time, stationId):
        EventQueue.push(
            Event(
                EventType.DROP_STATION,
                time,
                2,
                self.nextStation,
                StationEventArgs(stationId, time, self.name)
            )
        )

    def nextStation(self, args):
        EventQueue.push(
            Event(
                EventType.ENTER_STATION,
                args.time,
                2,
                self.arriveStation,
                StationEventArgs(args.stationId + 1, args.time, self.name),
            )
        )

    def queue(self, args):
        stationVisit = self.stationVisits[args.stationId]
        time = args.time + stationVisit.queuedServingTime()
        stationVisit.queue(args.customerName)

        self.enterStation(args.stationId, time)

    def enterStation(self, stationId, time):
        EventQueue.push(
            Event(EventType.ENTER_STATION, time, 2, self.serve, StationEventArgs(stationId, time, self.name))
        )

    def serve(self, args):
        stationVisit = self.stationVisits[args.stationId]
        
        time = args.time + stationVisit.servingTime()
        stationVisit.unqueue(self.name)
        EventQueue.push(
            Event(
                EventType.LEAVE_STATION, time, 1, self.leaveStation, StationEventArgs(args.stationId, time, self.name)
            )
        )

    def leaveStation(self, args):
        if args.stationId + 1 != len(self.stationVisits):
            self.arriveStation(StationEventArgs(args.stationId + 1, args.time, self.name))

    def startEvent(self):
        EventQueue.push(
            Event(
                EventType.START_SHOPPING,
                self.startTime,
                0,
                self.arriveStation,
                StationEventArgs(0, self.startTime, self.name),
            )
        )

    def copy(self):
        return Customer(self.name, self.stationVisits, self.startTime, self.spawnTime)

    def spawnNext(self):
        nextSpawnTime = self.startTime + self.spawnTime

        if self.startTime >= terminationTime:
            return

        nameSplit = self.name.split("-")
        name = f"{nameSplit[0]}-{str(int(nameSplit[1])+1)}"

        EventQueue.push(
            Event(
                EventType.SPAWN_CUSTOMER,
                nextSpawnTime,
                0,
                self.spawnCustomer,
                SpawnCustomerEventArgs(nextSpawnTime, name),
            )
        )

    def spawnCustomer(self, args):
        customer = self.copy()
        customer.name = args.customerName
        customer.startTime = args.time
        customer.startShopping()
