import numpy as np
import socket
from struct import unpack, pack

class Server:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', 5000))
        self.serverSocket.listen(1)
        print('The server is ready to receive')

    def encodeString(self, str):
        return str.encode('utf-8')

    def decodeString(self, str):
        return str.decode('utf-8')

    def close(self, connectionSocket):
        connectionSocket.close()

    def do(self):
        while True:
            connectionSocket, _ = self.serverSocket.accept()
            (id, result) = self.getMsg(connectionSocket)
            self.sendMsg(connectionSocket, id, result)
            self.close(connectionSocket)

    def sendMsg(self, connectionSocket, id, result):
        formatted = self.formatResult(id, result)
        connectionSocket.send(formatted)

    def formatResult(self, id, result):
        # format: <ID><Ergebnis>
        # ID is unsigned int 4 bytes (I)
        # Ergebnis = unsigned int.(I)
        return pack("II", id, result)

    # recive msg
    def getMsg(self, connectionSocket):
        msg = connectionSocket.recv(2048)
        part = unpack(f'IB', msg[0:5])
        id = int(part[0])
        s = int(part[1])
        print(part)
        partTwo = unpack(f'{s}sB', msg[5: 5 + s + 1])
        print(partTwo)
        calcType = partTwo[0].decode('utf-8')
        n = partTwo[1]
        print( msg[5 + s + 1:])
        values = unpack(f'{n}i', msg[5 + s + 2:])
        print(n, id, calcType, values)
        result = self.calculate(calcType, values)
        print(result)
        return (id, result)

    # do calculation
    def calculate(self, calcType, listOfNum):
        
        if(calcType == "Summe"):
            print("summing")
            return np.sum(listOfNum)
        elif(calcType == "Produkt"):
            return np.prod(listOfNum)
        elif(calcType == "Minimum"):
            return np.min(listOfNum)
        elif(calcType == "Maximum"):
            return np.max(listOfNum)

server = Server()
server.do()