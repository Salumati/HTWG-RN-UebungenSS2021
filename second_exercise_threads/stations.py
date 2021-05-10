from station import Station
from threading import Event

stopEv = Event()
entrance = Station("Eingang", stopEv)
bakery = Station("Bäcker", stopEv, 10)
sausage = Station("Wurst", stopEv, 30)
cheese = Station("Käse", stopEv, 60)
checkout = Station("Kasse", stopEv, 5)
outrance = Station("Ausgang", stopEv)

Stations = {
    "Eingang": entrance,
    "Bäcker": bakery,
    "Wurst": sausage,
    "Käse": cheese,
    "Kasse" : checkout,
    "Ausgang": outrance
}

def StartStations():
    global Stations
    for station in Stations:
        Stations[station].start()

def StopStations():
    global stopEv
    stopEv.set()