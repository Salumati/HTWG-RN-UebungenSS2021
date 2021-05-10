from enum import Enum


class EventType(Enum):
    START_SHOPPING = 1
    ENTER_STATION = 2
    LEAVE_STATION = 3
    SPAWN_CUSTOMER = 4
    QUEUE_CUSTOMER = 5
    DROP_STATION = 6

id = 0


class StationEventArgs:
    def __init__(self, stationId, time, customerName):
        self.stationId = stationId
        self.time = time
        self.customerName = customerName


class SpawnCustomerEventArgs:
    def __init__(self, time, customerName):
        self.time = time
        self.customerName = customerName


class QueueCustomerEventArgs:
    def __init__(self, stationId, time, customerName):
        self.stationId = stationId
        self.time = time
        self.customerName = customerName


class Event:
    def __init__(self, type, time, priority, func, args):
        global id

        self.type = type
        self.time = time
        self.priority = priority
        self.id = id
        self.func = func
        self.args = args

        id += 1

    def execute(self):
        self.func(self.args)

    def __lt__(self, other):
        return (self.time, self.priority, self.id) < (other.time, other.priority, other.id)

    def __str__(self):
        if isinstance(self.args, StationEventArgs):
            return f"Event: {self.type}, Time: {self.time}, {self.priority}, {self.id}, StationId: {self.args.stationId}, {self.args.customerName}"
        else:
            return f"Event: {self.type}, Time: {self.time}, {self.priority}, {self.id}, {self.args.customerName}"
