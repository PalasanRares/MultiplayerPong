import socket
import json
import struct
import sys
import random
from threading import Thread
from player import Player
from room_thread import RoomThread

NEW_ROOM = -1

def read_from_file(file_name):
    ip_and_port = json.load(open(file_name))
    return ip_and_port["localIp"], ip_and_port["localPort"]


def generate_room_number(room_numbers):
    number = random.randrange(0, 10000)
    while number in room_numbers:
        number = random.randrange(0, 10000)
    return number


def run():
    local_ip, local_port = read_from_file("server_address.json")

    tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((local_ip, local_port))
    print("Server is up and waiting for connections!")

    room_numbers = []
    threads = {}

    while True:
        tcp_socket.listen()
        (client_connection, (client_ip, client_port)) = tcp_socket.accept() # new client connected
        (room_number,) = struct.unpack("!i", client_connection.recv(4)) # receive the room number
        new_client = Player(client_ip, client_port, client_connection)

        # checking if the room exists or a new room should be created
        if (room_number == NEW_ROOM):
            new_room_number = generate_room_number(room_numbers)
            room_numbers.append(new_room_number)
            room_thread = RoomThread(new_client, new_room_number)
            threads[new_room_number] = room_thread
            client_connection.send(struct.pack("!i", 200)) # sending success to player that created the room
        else:
            if room_number in room_numbers and threads[room_number].add_second_player(new_client):
                client_connection.send(struct.pack("!i", 200)) # sending succes to player that joined the room
                threads[room_number].start()
            else:
                print("Client " + client_ip + " tried to connect to a non existing or full room")
                client_connection.send(struct.pack("!i", 400)) # sending error to player that tried joining the room


if (__name__ == "__main__"):
    run()