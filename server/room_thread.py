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

    
    # this function runs when the thread is started
    # it should connect the client to one another and then stop
    def run(self):
        # player1 sends a port to the server, that forwards it to player2
        # player1 will start acting as a server for the p2p connection between the two
        (p2p_port,) = struct.unpack("!i", self.__player1.get_connection().recv(4))

        # sending the ip and port of player1 to player2
        self.__player2.get_connection().send(self.__player1.get_ip().encode())
        self.__player2.get_connection().send(struct.pack("!i", p2p_port))

        # closing the connection between the players and the server
        self.__player1.get_connection().close()
        self.__player2.get_connection().close()

    
    def add_second_player(self, player2):
        if (self.__player2 == None):
            self.__player2 = player2
            print("New client added to room " + str(self.__room_number) + " ip " + player2.get_ip() + " port " + str(player2.get_port()))
            return True
        return False


    def get_player1(self):
        return self.__player1


    def get_player2(self):
        return self.__player2

    
    def get_room_number(self):
        return self.__room_number