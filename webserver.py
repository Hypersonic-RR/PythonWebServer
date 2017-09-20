#import socket module
from socket import *
import sys # In order to terminate the program
import thread
from socket import error as socket_error
import errno

clients = []

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('192.168.0.12',3030))
serverSocket.listen(5)
#Establish the connection

def handler(clientsock, addr):
    while 1:
        try:
            data = clientsock.recv(1024)
        except socket_error as serr:
            if serr == errno.ECONNREFUSED or serr == errno.ECONNRESET:
                clients.pop(clientsock)
                thread.exit()
        for c in clients:
            if c != clientsock:
                try:
                    c.sendall(data)
                except socket_error as e:
                    if e == errno.EPIPE:
                        clients.pop(c)
        
def main():
    while 1:
        print '> waiting for connection...'
        connectionSocket, addr = serverSocket.accept()
        print '> connected from ', addr
        clients.append(connectionSocket)
        thread.start_new_thread(handler, (connectionSocket, addr))

if __name__ == "__main__":
    main()