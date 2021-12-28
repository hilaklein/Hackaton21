import socket
import struct

PORT = 13117
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2
MESSAGE_SIZE = 1024


team_name = "hereForThePizza"
class Client:
    def __init__(self):
        self.client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # udp socket
        self.client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # enable broatcat
        self.client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # enable reuse address

        self.client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp socket
        self.client_tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # enable reuse
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.team_name = "firstClient"

    def looking_for_a_server(self):  # waiting for offers
        try:
            self.client_udp_socket.bind(('',PORT))
            print("Client started, listening for offer requests...")
            message, addr = self.client_udp_socket.recvfrom(MESSAGE_SIZE)
            magic_cookie, message_type, port = struct.unpack('IBH', message)
            if (magic_cookie == MAGIC_COOKIE) and (message_type == MESSAGE_TYPE):
                print("Received offer from " + addr[0] + ", attempting to connect...")
                self.connecting_to_server(addr[0], port)
            else:
                print("The message is not in the right format")

        except Exception as ex:
            print (ex)
            print (ex.args)
            print (ex.with_traceback())

    def connecting_to_server(self, ip, port):
        try:
            self.client_tcp_socket.connect((ip, port))
            team_name_n = self.team_name + "\n"  # add end to name
            team_name_encoded = team_name_n.encode('UTF-8')  # encode before send
            self.client_tcp_socket.send(team_name_encoded)  # send encoded message
            self.game_mode((ip, port))
        except Exception as ex:
            print (ex)

    def game_mode(self, addr):
        try:
            welcome_mess = self.client_tcp_socket.recv(MESSAGE_SIZE).decode()  # get welcoming to game message from server
            print(welcome_mess)
            math_mess = self.client_tcp_socket.recv(MESSAGE_SIZE).decode()  # mathematical question
            print(math_mess)
            answer = input("answer: ")
            self.client_tcp_socket.send(answer.encode('UTF-8'))
            print(self.client_tcp_socket.recv(MESSAGE_SIZE).decode())  # end of game message
            print("Server disconnected, listening for offer requests...")
            self.looking_for_a_server()
        except Exception as ex:
            pass




if __name__ == '__main__':
    cleint1 = Client()
    cleint1.looking_for_a_server()

