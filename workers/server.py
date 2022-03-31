import socket
import time

from .utils import encode_content


class UDPServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self, host: str, port: int):
        while 1:
            try:
                self.server.bind((host, port))
            except:
                print("ohhhhhhhhhhhhhhhhhhhhhh!")
                time.sleep(10)
            while 1:
                data = self.server.recvfrom(1024)
                print("recv: ", data)
                self.server.sendto(encode_content("hi. I'm woring~"), data[-1])
                time.sleep(0.01)
