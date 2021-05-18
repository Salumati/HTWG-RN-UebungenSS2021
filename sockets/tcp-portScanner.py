from threading import Thread, Event, Lock
import socket
# gibt die Anzahl der offenen TCP-Ports auf gegebenen Server zurück

socket.setdefaulttimeout(10)

ip = '141.37.168.26'  # ausfuehrung auf Labor-Server 141.37.168.26
portRange = 50  # Ports zwischen 1 und 50
openPorts = 0
globalLock = Lock()
# continueEvent = Event()

def countPorts():
    globalLock.acquire()
    global openPorts
    openPorts += 1
    globalLock.release()

def checkConnection(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.connect((ip, port))
        print(f'connection to port {port} was successful!')
        countPorts()
    except socket.timeout:
        print(f'connection to port {port} was unsuccessful.')
    skt.close()


def startThreads():
    threads = []
    print("starting threads:")
    for i in range(portRange):
        t = Thread(target=checkConnection, args=(i+1,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

startThreads()

print(f'number of open ports: {openPorts}')

# starte die einzelenn Port-Anfragen als Threads, um den Scan-Vorgang zu beschleunigen

# t=Thread(target=<function>,args=(<arg>,))
# beenden durch globale flag continue

