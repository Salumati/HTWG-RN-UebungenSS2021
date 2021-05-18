import socket
from struct import unpack, pack

IPadrr = "127.0.0.2"
port = 5000
tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

class Client:

    def __init__(self, ip=IPadrr, port=port, socketType=tcp) :
        self.clientSocket = socket.socket(socket.AF_INET, socketType)
        self.ip = ip
        self.port = port
        self.socketType = socketType

    def do(self):
        if self.socketType == tcp:
            self.connectToServer()
        while True:
            self.sendMsg()
            self.getMsg()
            print("'enter' to continue or 'q' to quit")
            if input() == "q":
                break
        self.close()

    def formatMsg(self, msg):
        # format: <ID><Rechenoperation><N><z1><z2>...<zN>
        
        # ID is unsigned int 4 bytes (I)
        # Rechenop is String in UTF 8 (s)
        # N is unsigned-char, defining how many num will follow (B)
        # <z1>...<zn> values  for Calulations, signed Integer (i)

        # split msg in its parameter:
        splitMsg = msg.split(" ", 3)
        id = int(splitMsg[0])
        calc = splitMsg[1]
        n = int(splitMsg[2])
        listOfNum = list(map(int, splitMsg[3].split(" ")))
        return pack(f'=IBB{len(calc)}s{n}i', id, len(calc), n, calc.encode('utf-8'), *listOfNum)

    def sendMsg(self):
        print("please enter math operation in format:\n <ID> <calculation> <numbersOfvalues> <values>")
        msg = input()
        msg = self.formatMsg(msg)
        if self.socketType == tcp:
            self.clientSocket.sendall(msg)
        elif self.socketType == udp:
            self.clientSocket.sendto(msg, (self.ip, self.port))

    def getMsg(self):
        # format: <ID><Ergebnis>
        # ID is unsigned int 4 bytes (I)
        # Ergebnis = unsigned int.(I)
        if self.socketType == tcp:
            result = self.clientSocket.recv(2048)
        elif self.socketType == udp:
            result, _ = self.clientSocket.recvfrom(2048)
        result = unpack("II", result)
        print(f'result is:\n {result[1]}')

    # establish connection
    def connectToServer(self):
        self.clientSocket.connect((self.ip, self.port))

    def close(self):
        self.clientSocket.close()

client = Client()
client.do()