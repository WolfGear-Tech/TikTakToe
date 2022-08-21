from socket import *
#from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread

class ClientSocketHandler():

    def __init__(self):
        self.SERVER_ADDR = (gethostbyname("otoma.solutions"), 8090)
        self.ENCODE_FORMAT = "utf-8"
        self.DISCONECT_MESSAGE = "!DISCONNECT"
        self.HANDLE_CONNECTION = True
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.SERVER_ADDR)

    def SendMessage(self, message):
        print(f"[SEND] - Sending the message: {message} to the server")
        self.clientSocket.send(message.encode(self.ENCODE_FORMAT))
        if message == self.DISCONECT_MESSAGE:
            self.HANDLE_CONNECTION = False

    def ResponseListener(self):
        while self.HANDLE_CONNECTION:
            recivedMessage = self.clientSocket.recv(2048).decode(self.ENCODE_FORMAT)
            if recivedMessage != self.DISCONECT_MESSAGE:
                print(f"[MESSAGE RECIVED] - New Message reciver from client the new message is: {recivedMessage}")        
            else:
                self.HANDLE_CONNECTION = False
                print(f"[DISCONNECT] - Closing the connection thread !!")
                break
        self.clientSocket.close()
        exit()

    def StartSocket(self):
        Thread(target=self.ResponseListener, daemon=True).start()
        while self.HANDLE_CONNECTION:
            message = input("Enter your message: ")
            self.SendMessage(message)

conn = ClientSocketHandler()
conn.StartSocket()