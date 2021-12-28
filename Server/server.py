import socket
import struct
import threading
from threading import *
import random
import time
import scapy.arch

UDP_DEST_PORT = 13117
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE = 0x2
MESSAGE_SIZE = 2048
my_tcp_port = 7000
dest_tcp_port = 5000
is2connected = True



class Server:
    def __init__(self):
        self.server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp socket
        self.server_tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.team_names = []
        self.recv_threads = []
        self.games_threads = []
        self.local_udp_ip = '255.255.255.255'
        # self.local_tcp_ip = scapy.arch.get_if_addr("eth1")
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp socket
        self.server_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # enable reuse address
        self.server_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # enable broatcat
        self.random_nums = self.generate_math_question()
        self.numConnected = 0
        self.is_answered = False
        self.winner = ""
        self.lock = threading.Lock()

    def Waiting_for_clients(self):

        try:
            self.server_udp_socket.bind(('',UDP_DEST_PORT))
            self.server_tcp_socket.bind(('', my_tcp_port))  # change
            print("Server started, listening on IP address ", self.local_udp_ip) #change
            offer_thread = Thread(target=self.broadcast_offers, daemon=True)
            offer_thread.start()
            recieve_thread = Thread(target=self.recieve_clients(),daemon=True)
            recieve_thread.start()

            # while True:
            #     (conn, (dest_ip, dest_port)) = self.server_tcp_socket.accept()
            #     recieve_client = Thread(target=self.recieve_clients,args=(conn),daemon=True)
            #     game_thread = Thread(target=self.game_mode,args=(conn),daemon=True)
            #     self.recv_threads.append(recieve_client)
            #     self.games_threads.append(game_thread)
            #     self.numConnected =self.numConnected+1
            #     if self.numConnected == 2:
            #
            #         self.is2connected = False
            #         for t in self.recv_threads:
            #             t.start()
            #             t.join()
            #         for t in self.games_threads:
            #             t.start()
            #             t.join(10)
            #         break

        except Exception as ex:
            print(ex)

    def generate_math_question(self):
        a = random.randint(0,9)
        b = random.randint(0,(9-a))
        return [a,b]
    def end_game(self,team,conn):
        if self.is_answered:
            return
        else :
            self.is_answered = True
            self.winner = "the winner is " + team


    def broadcast_offers(self):
        while is2connected:
                self.server_udp_socket.sendto((struct.pack('IBH', MAGIC_COOKIE, MESSAGE_TYPE, my_tcp_port)),
                ('<broadcast>', UDP_DEST_PORT))
                time.sleep(1)
    def recieve_clients(self):
        self.server_tcp_socket.listen(2)
        while True:
            (conn, (dest_ip, dest_port)) = self.server_tcp_socket.accept()
            data = conn.recv(MESSAGE_SIZE).decode()  # get team name
            self.team_names.append(data)
            game_thread = Thread(target=self.game_mode, daemon=True, args=[conn,data])
            self.games_threads.append(game_thread)
            self.numConnected = self.numConnected + 1
            if self.numConnected == 2:
                self.is2connected = False
                for t in self.games_threads:
                    t.start()
                for t in self.games_threads:
                    t.join(10)
                break

    def game_mode(self,conn,team):
        welcome_message = "Welcome to Quick Maths\n"+ "Player 1: "+ self.team_names[0]+ "Player 2: "+self.team_names[1]+ "\n=="
        answer = self.random_nums[0] + self.random_nums[1]
        math_question_message = "How much is "+ str(self.random_nums[0])+ "+"+ str(self.random_nums[1])
        conn.send(welcome_message.encode())
        conn.send(math_question_message.encode())
        client_answer = conn.recv(MESSAGE_SIZE).decode()  # get answer
        self.lock.acquire()
        if int(client_answer) == answer:
            self.end_game(team,conn)
        conn.send(self.winner.encode())
        self.lock.release()
        if self.is_answered:
            conn.shutdown(socket.SHUT_RD)
            conn.close()



if __name__ == '__main__':
    s = Server()
    s.Waiting_for_clients()
