import socket
from struct import pack, unpack

client_ip = '127.0.0.2'

# formats:
f_chat = "124s"
f_chatP = "32s10sii32s10s"
f_login = "32s10si"
f_logout = "32s102i"
f_broadcast = f"32s10si124s"
f_listrequ = f"32s10si"
f_update = "32s10si32s10s"

# values
v_login = 0
v_listrequ = 1
v_chatrequ = 2
v_logout = 4
v_brodcast = 5

class ChatServer:
    def __init__(self):
        self.clients = {}  # dictionary of clients
        self.my_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        print(f"Starting server.\nHello!")
        self.bind_tcp()
        self.listen(5)  # allows max 5 connections.
        # prbably need threading later, so I can listen to udp as well
        while(True):
            (client_socket, adresse) = self.my_TCP_socket.accept()
            # remember to flush sockets between reads!
            # send returns when the associated network buffers have been filled.
            # recv returns when the associated network buffers have been emptied.
            # if recv returns 0 bytes, the other side has been closed.

            # to properly handle a message: it needs a fixed lenght, tell you it's lenght
        self.end()

    def end(self):
        self.my_TCP_socket.close()
        self.my_UDP_socket.close()
        print("Sockets Closed.\nGoodbye.")

    def bind_tcp(self, port=80):
        self.my_TCP_socket.bind((socket.gethostname(), port))
        # gethostname makes it visibil to the outside
        # 80 makes it so that only ports on the same machine can access this

    def send_msg(self, msg_format, msg):
        packed_msg = pack(msg_format, msg)
        self.my_TCP_socket.send(packed_msg)

    def recive_msg(self):
        # get msg
        msg = self.my_TCP_socket.recv(2048)
        if not msg:
            print("recived empty msg")
            # self.end()
        ip = unpack(f'32s', msg[:32])
        print(ip)
        name = unpack(f'10s', msg[33:43])
        print(name)
        requ = unpack(f'i', msg[44])
        self.decode(requ, (ip, name), msg[45:])

    def decode(self, code, client_ip, client_name, arg):
        if code == f_login:
            self.log_client_in(client_ip, client_name, arg)
        if code == f_listrequ:
            self.send_client_list(client_ip, client_name)
        if code == f_chatP:
            self.activate_chat(client_ip, client_name, arg)
        if code == f_update:
            self.update_clients()
        if code == f_logout:
            self.log_client_out()
        if code == f_broadcast:
            msg = unpack(f'124s', arg)
            self.boradcast(msg)

    # log in client
    def log_client_in(self, client_ip, client_name, client_udp):
        # check if name
        client = (client_ip, client_name, client_udp)
        self.clients.update(client_name, client)

    # send list of users
    def send_client_list(self, mdata):
        lst = str(self.clients).split('{')[1].split('}')[0]
        n = len(lst)
        msg_format = f_listrequ + str(n) + lst
        self.send_msg(msg_format, lst)

    # update clients
    def update_clients(self):
        for c in self.clients:
            print(c)

    # establish communication between clients
    def activate_chat(self, client1, client2):
        return

    # logout client
    def log_client_out(self, client_name):
        del self.clients[client_name]
        self.clients.update(client_name)
        # send affirmation message

    # broadcast
    def boradcast(self, msg):
        packed_msg = pack(f_broadcast, msg)
        for c in self.clients:
            self.send_msg(msg)

    # remember error handeling!


server = ChatServer()
server.run()
