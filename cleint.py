

import struct
from socket import *

PORT = 13117
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2
MESSAGE_SIZE = 1024

team_name = "hereForThePizza"
class Client:
    def _init_(self):
        self.client_udp_socket = socket(AF_INET, SOCK_DGRAM)  # udp socket
        self.client_udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # enable reuse address
        self.client_udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # enable broatcat
        self.client_tcp_socket = socket(AF_INET, SOCK_STREAM)  # tcp socket
        self.client_tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # enable reuse

    def looking_for_a_server(self):  # waiting for offers
        try:
            self.client_udp_socket.bind(PORT)
            print("Client started, listening for offer requests...")
            message, addr = self.client_udp_socket.recvfrom(MESSAGE_SIZE)
            magic_cookie, message_type, port = struct.unpack("IBH", message)
            magic_Hex = hex(magic_cookie)
            if (magic_Hex & MAGIC_COOKIE == MAGIC_COOKIE) and (message_type == MESSAGE_TYPE):
                print("Received offer from" + addr[0] + ",attempting to connect...")
                self.connecting_to_server(addr[0], port)
            print("The message is not in the right format")

        except Exception as ex:
            pass

    def connecting_to_server(self, ip, port):
        try:
            self.client_tcp_socket.connect(ip, port)
            team_name_n = self.team_name + "\n"  # add end to name
            team_name_encoded = team_name_n.encode('UTF-8')  # encode before send
            self.client_tcp_socket.sendto(team_name_encoded)  # send encoded message
            self.game_mode((ip, port))
        except Exception as ex:
            pass

    def game_mode(self, addr):
        try:
            print(self.client_tcp_socket.recv(MESSAGE_SIZE).decode())  # get welcoming to game message from server
            print(self.client_tcp_socket.recv(MESSAGE_SIZE).decode())  # mathematical question
            answer = input("answer: ")
            self.client_tcp_socket.send(answer.encode('UTF-8'))
            print(self.client_tcp_socket.recv(MESSAGE_SIZE).decode())  # end of game message
            print("Server disconnected, listening for offer requests...")
            self.looking_for_a_server()
        except Exception as ex:
            pass

cleint = Client()



while(True):
    cleint.looking_for_a_server()

