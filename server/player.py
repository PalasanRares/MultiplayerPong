class Player:

    def __init__(self, ip, port, connection):
        self.__ip = ip
        self.__port = port
        self.__connection = connection

    
    def get_ip(self):
        return self.__ip

    
    def get_port(self):
        return self.__port
    

    def get_connection(self):
        return self.__connection