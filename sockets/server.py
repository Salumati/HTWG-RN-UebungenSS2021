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

            result = self.getMsg(connectionSocket)
            #self.sendMsg(connectionSocket, result)
            self.close(connectionSocket)

    def sendMsg(self, connectionSocket, result):
        formatted = self.encodeString(self.formatResult(result))
        connectionSocket.send(formatted)

    def formatResult(id, msg):
        # format: <ID><Ergebnis>
        # ID is unsigned int 4 bytes (I)
        # Ergebnis = unsigned int.(I)
        return pack("II", id, msg)

    # recive msg
    def getMsg(self, connectionSocket):
        msg = self.decodeString(connectionSocket.recv(1024))
        print(msg[0:2])
        part = unpack(f'I10sBi', msg[0:4])

        #unpacked = unpack(f'{part[-1]}i', msg[4:])
        #return self.calculate({unpacked[1]}, )

    # do calculation
    def calculate(type, listOfNum):
        if(type == "Summe"):
            return np.sum(listOfNum)
        elif(type == "Produkt"):
            return np.prod(listOfNum)
        elif(type == "Minimum"):
            return np.min(listOfNum)
        elif(type == "Maximum"):
            return np.max(listOfNum)

server = Server()
server.do()