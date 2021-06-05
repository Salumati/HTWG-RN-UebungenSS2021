import socket
from struct import pack, unpack

server_ip = '127.0.0.1'
local_ip = '127.0.0.1'
port = 5000

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

class ChatClient:
    def __init__(self):
        self.my_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.name = "client1"
        self.my_ip = local_ip
        self.my_tcp.bind(server_ip, port)

    def run(self):
        print(f"starting client.\nHello")
        self.my_tcp.connect((server_ip, port))
        self.log_in()
        self.log_out()
        self.end()

    def end(self):
        self.my_tcp.close()
        self.my_udp.close()
        print("Goodbye")

    def decode(self, code, client_ip, client_name, arg):
        if code == f_login:
            self.log_in(client_ip, client_name, arg)
        if code == f_listrequ:
            self.rqu_client_list(client_ip, client_name)
        if code == f_chatP:
            self.activate_chat(client_ip, client_name, arg)
        if code == f_update:
            self.update_self()
        if code == f_logout:
            self.log_out()
        if code == f_broadcast:
            msg = unpack(f'124s', arg)
            self.rcv_boradcast(msg)


    # log into server
    def log_in(self):
        try:
            msg = "hello, I am client"
            self.my_tcp.send(pack(f"{len(msg)}s", msg))
        except socket.timeout:
            print("log in fehlgeschlagen")

    # log out of server
    def log_out(self):
        msg = pack(f_logout, self.my_ip, self.adjust_name(), v_logout)
        self.my_tcp.send(msg)

    # request list of chat clients
    def rqu_client_list(self):
        print("requesting list")
        return

    # request connection to other client
    def activate_chat(self, client_name, arg):
        return

    # send broadcast
    def send_boradcast(self, msg):
        return

    # recive broadcast
    def rcv_broadcast(self, msg):
        return

    def adjust_name(self):
        return self.name.ljust(10, '0')