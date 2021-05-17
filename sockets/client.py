import socket
from struct import unpack, pack

IPadrr = "127.0.0.2"
port = 5000


class Client:

    def __init__(self, ip=IPadrr, port=port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def encodeString(self, str):
        return str.encode('utf-8')

    def decodeString(self, str):
        return str.decode('utf-8')

    def do(self):
        self.connectToServer()
        self.sendMsg()
        self.getMsg()
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
        print(listOfNum)
        return pack(f'I10sB{n}i', id, bytes(calc, 'utf-8'), n, *listOfNum)

    def sendMsg(self):
        print("please enter math operation in format:\n <ID> <calculation> <numbersOfvalues> <values>")
        msg = input()
        msg = self.formatMsg(msg)
        print(f'message is: {msg}')
        self.clientSocket.sendAll(msg)

    def getMsg(self):
        # format: <ID><Ergebnis>
        # ID is unsigned int 4 bytes (I)
        # Ergebnis = unsigned int.(I)
        msg = self.clientSocket.recv(1024)
        print(f'laenge der nachricht: {len(msg)}')
        result = unpack("II", msg)
        print(f'result is:\n {result[1]}')

    # establish connection
    def connectToServer(self):
        self.clientSocket.connect((self.ip, self.port))

    def close(self):
        self.clientSocket.close()


client = Client()
client.do()