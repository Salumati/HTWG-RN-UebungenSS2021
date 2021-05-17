import socket
import base64
from struct import unpack, pack

IPadrr = "127.0.0.1"


class Client:
    def __init__(self, ip=IPadrr, port=80):
        self.clientSocket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.bind(ip, port)

    def encodeString(self, asciStr):
        return (base64.b64encode(asciStr.encode('utf-8'))).decode('utf-8')

    def decodeString(self, base64):
        return (base64.b64decode(base64)).decode('utf-8')

    def formatMsg(self, msg):
        # format: <ID><Rechenoperation><N><z1><z2>...<zN>
        # ID is unsigned int 4 bytes (I)
        # Rechenop is String in UTF 8 (s)
        # N is unsigned-char, defining how many num will follow (B)
        # <z1>...<zn> values  for Calulations, signed Integer (i)

        # split msg in its parameter:
        splitMsg = msg.split(" ", 3)
        id = splitMsg[0]
        calc = (base64.b64encode(splitMsg[1].encode('utf-8'))).decode('utf-8')
        n = splitMsg[2]
        listOfNum = splitMsg[3]
        return pack("IsBii", id, calc, n, listOfNum)

    def sendMsg(self):
        print("please enter math operation in format:\n <ID> <calculation> <numbersOfvalues> <values>")
        msg = input()
        msg = self.formatMsg(msg)
        self.clientSocket.send(msg)

    def getMsg(self, msg):
        # format: <ID><Ergebnis>
        # ID is unsigned int 4 bytes (I)
        # Ergebnis = unsigned int.(I)

        result = unpack("II", msg)
        print(f'result is:\n {result[1]}')

    # establish connection
    def connectToServer(self):
        return
