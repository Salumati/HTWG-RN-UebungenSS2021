from threading import Thread, Event, Lock
import socket
# gibt die Anzahl der offenen UDP- oder TCP-Ports auf gegebenen Server zurück

# socket.setdefaulttimeout(30)

ip = '141.37.168.26'  # ausfuehrung auf Labor-Server 141.37.168.26
portRange = 50  # Ports zwischen 1 und 50
openTCP = 0
openUDP = 0
tcpLock = Lock()
udpLock = Lock()
# continueEvent = Event()

def countTCPPorts():
    tcpLock.acquire()
    global openTCP
    openTCP += 1
    tcpLock.release()

def countUDPPorts():
    udpLock.acquire()
    global openUDP
    openUDP += 1
    udpLock.release()

def winErrorHandling(we, type, port):

    if we == 10054:
        print(f'connection to {type} port {port} was unsuccessful, server did not answer .')
        return
    if we == 10060:
        print(f'connection to {type} port {port} was unsuccessful, server timeout .')
        return
    if we == 10061:
        print(f'connection to {type} port {port} was unsuccessful, connection was rejected.')
        return
    print(f'connection to {type} port {port} had unscpecified windows error:\n {we}.')


def checkUDP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    type = "UDP"
    try:
        #print(f'connection to {type} port {port}')
        skt.sendto("Hello World!".encode('utf-8'), (ip, port))
        data, addr = skt.recvfrom(1024)
        print("udp", data, "port", port)
        countUDPPorts()
    except socket.timeout:
        #print(f'connection to {type} port {port} was unsuccessful due to timeout.')
        print("")
    except WindowsError as we:
        print("")
        #print(f'connection to {type} port {port} had windows error:\n {we}.')

    skt.close()


def checkTCP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    type = "TCP"
    try:
        #print(f'connection to {type} port {port}')
        skt.connect((ip, port))
        #print(f'connection to {type} port {port} was successful! sending Message')
        skt.send("Hello World!".encode('utf-8'))
        data = skt.recv(1024)
        print("tcp", data, "port", port)
        countTCPPorts()
    except socket.timeout:
        print("")
        #print(f'connection to {type} port {port} was unsuccessful due to timeout.')
    except WindowsError as we:
        print("")
        #winErrorHandling(we, type, port)

    skt.close()

def checkConnection(port):
    checkTCP(port)
    checkUDP(port)



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

print(f'number of open UDP ports: {openUDP}')
print(f'number of open TCP ports: {openTCP}')

# starte die einzelenn Port-Anfragen als Threads, um den Scan-Vorgang zu beschleunigen

# t=Thread(target=<function>,args=(<arg>,))
# beenden durch globale flag continue