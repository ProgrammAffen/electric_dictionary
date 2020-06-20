'''
客户端业务逻辑层
'''
from socket import *
import sys
class ClientController:
    def __init__(self):
        self.create_socket()
        self.bind()
        self.dir = dir
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    def bind(self):
        server_addr = ('127.0.0.1', 6666)
        self.sockfd.connect(server_addr)
    def register(self,name,password):
        msg = 'R ' + name + ' ' + password
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'Username exists':
            return False
        else:
            return True
    def log_in(self,name,password):
        msg = 'LI ' + name + ' ' + password
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'Log in suceeded':
            return True
        else:
            return False
    def log_out(self):
        msg = 'Q quit'
        self.sockfd.send(msg.encode())
        sys.exit('log out,bye')
    def find_word(self,name,word):
        msg = 'C ' + name + ' ' + word
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'not find':
            return False
        else:
            return data
    def get_history(self,name):
        msg = 'C ' + name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == 'Unknown Error':
            return False
        else:
            return data