import socket
import json
import struct
import sys
from threading import Thread


class ClientThread(Thread):

    def __init__(self, ip, port, connection):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.connection = connection
        print("New thread created for ip " + ip + " port " + str(port))

    
    def run(self):
        (data,) = struct.unpack("!i", self.connection.recv(1024)) # struct.unpack returns a tuple containing one item
        print("Received " + str(data) + " from client")
    

def read_from_file(file_name):
    ip_and_port = json.load(open(file_name))
    return ip_and_port["localIp"], ip_and_port["localPort"]


def run():
    local_ip, local_port = read_from_file("server_address.json")

    tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((local_ip, local_port))
    print("Server is up and waiting for connections!")

    threads = []

    while True:
        tcp_socket.listen()
        (client_connection, (client_ip, client_port)) = tcp_socket.accept()
        new_client = ClientThread(client_ip, client_port, client_connection)
        new_client.start()
        threads.append(new_client)


if (__name__ == "__main__"):
    run()