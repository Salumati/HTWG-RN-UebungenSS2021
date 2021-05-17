import socket
import base64
from struct import unpack, pack

IPadrr = "127.0.0.1"


class Server:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((socket.gethostname(), 80))

    def listen(self):
        self.serverSocket.listen(5)
