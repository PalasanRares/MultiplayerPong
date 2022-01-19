import socket
import struct
import threading
from threading import Thread
from player import Player

class RoomThread(Thread):

    def __init__(self, player1,  room_number):
        Thread.__init__(self)
        self.__player1 = player1
        self.__player2 = None
        self.__room_number = room_number
        print("New room created, room " + str(room_number) + " ip " + player1.get_ip() + " port " + str(player1.get_port()))

    
    def run(self):
        (data,) = struct.unpack("!i", self.__player1.get_connection().recv(1024)) # struct.unpack returns a tuple containing one item
        print("Received " + str(data) + " from client")

    
    def add_second_player(self, player2):
        if (self.__player2 == None):
            self.__player2 = player2
            print("New client added to room " + str(self.__room_number) + "ip " + player2.get_ip() + " port " + str(player2.get_port()))


    def get_player1(self):
        return self.__player1


    def get_player2(self):
        return self.__player2

    
    def get_room_number(self):
        return self.__room_number