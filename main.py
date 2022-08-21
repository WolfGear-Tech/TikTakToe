from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread

SERVER_ADDR = (gethostbyname(gethostname()), 8090)
ENCODE_FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
HANDLE_CONNECTION = True
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(SERVER_ADDR)

def Send(message):
    print(f"[SEND] - Sending the message: {message} to the server")
    clientSocket.send(message.encode(ENCODE_FORMAT))

def ResponseListenerHandler():
    while HANDLE_CONNECTION:
        recivedMessage = clientSocket.recv(2048).decode(ENCODE_FORMAT)
        if recivedMessage != DISCONECT_MESSAGE:
            print(f"[MESSAGE RECIVED] - New Message reciver from client the new message is: {recivedMessage}")        
        else:
            print(f"[DISCONNECT] - Closing the connection thread !!")
            break
    clientSocket.close()
    exit()

Thread(target=ResponseListenerHandler, daemon=True).start()

while True:
    message = input("Enter your message: ")
    Send(message)