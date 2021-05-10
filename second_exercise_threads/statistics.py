from event import StationEventArgs, EventType
from station_visits import stationVisitsK1, stationVisitsK2
from math import floor

class Statistics:
    def __init__(self, eventHistory):
        self.eventHistory = eventHistory

    def lastServedCustomerTime(self):
        return self.eventHistory[-1].time
    
    def servedCustomers(self):
        eventuallyServedCustomers = []
        for event in self.eventHistory:
            if isinstance(event.args, StationEventArgs):
                customerType = event.args.customerName.split("-")[0]
                if (customerType == "K1" and event.args.stationId == len(stationVisitsK1)-1) or (customerType == "K2" and event.args.stationId == len(stationVisitsK2)-1):
                    eventuallyServedCustomers.append(event.args.customerName)

    
        return str(list(set(eventuallyServedCustomers) - set(self.droppedCustomers())))

    def completeShoppingTime(self):
        _droppedCustomers = self.droppedCustomers()

        eventuallyServedCustomerTimes = {}

        for event in self.eventHistory:
            if event.args.customerName not in _droppedCustomers:
                if event.type == EventType.START_SHOPPING:
                    if event.args.customerName not in eventuallyServedCustomerTimes:
                        eventuallyServedCustomerTimes.setdefault(event.args.customerName, [])
                    eventuallyServedCustomerTimes[event.args.customerName].append(event.time)
                elif event.type == EventType.LEAVE_STATION:
                    customerType = event.args.customerName.split("-")[0]
                    if (customerType == "K1" and event.args.stationId == len(stationVisitsK1)-1) or (customerType == "K2" and event.args.stationId == len(stationVisitsK2)-1):
                        if event.args.customerName not in eventuallyServedCustomerTimes:
                            eventuallyServedCustomerTimes.setdefault(event.args.customerName, [])
                        eventuallyServedCustomerTimes[event.args.customerName].append(event.time)

        servedCustomerTimes = [eventuallyServedCustomerTimes[customer] for customer in eventuallyServedCustomerTimes if customer not in _droppedCustomers]
        
        averageServedCustomerTime = 0
        for servedTime in servedCustomerTimes:
            averageServedCustomerTime += servedTime[1] - servedTime[0]
        
        return floor(averageServedCustomerTime / len(servedCustomerTimes))

    def stationCustomers(self, station):
        _stationCustomers = {}
        for event in self.eventHistory:
            if event.type == EventType.ENTER_STATION:
                customerType = event.args.customerName.split("-")[0]
                if(customerType == "K1"):
                    _station = stationVisitsK1[event.args.stationId]._station
                    if _station not in _stationCustomers:
                            _stationCustomers.setdefault(_station, [])
                    _stationCustomers[_station].append(event.args.customerName)
                elif(customerType == "K2"):
                    _station = stationVisitsK1[event.args.stationId]._station
                    if _station not in _stationCustomers:
                            _stationCustomers.setdefault(_station, [])
                    _stationCustomers[_station].append(event.args.customerName)
        return _stationCustomers[station]

    def droppedStationCustomers(self, station):
        _droppedStationCustomers = []
        _stationCustomers = self.stationCustomers(station)

        for event in self.eventHistory:
            if event.type == EventType.DROP_STATION:
                customerType = event.args.customerName.split("-")[0]
                _station = ""
                if(customerType == "K1"):
                    _station = stationVisitsK1[event.args.stationId]._station
                elif(customerType == "K2"):
                    _station = stationVisitsK2[event.args.stationId]._station
                if _station == station:
                    _droppedStationCustomers.append(event.args.customerName)
                    
        return set(_droppedStationCustomers).intersection(_stationCustomers)

    def droppedStationPercentage(self, station):
        _stationCustomers = self.stationCustomers(station)
        _droppedStationCustomers = self.droppedStationCustomers(station)

        return str(floor((len(_droppedStationCustomers) / len(_stationCustomers)) * 100)) + "%"

    def droppedCustomers(self):
        _droppedCustomers = []
        for event in self.eventHistory:
            if event.type == EventType.DROP_STATION:
                _droppedCustomers.append(event.args.customerName)
        return _droppedCustomers