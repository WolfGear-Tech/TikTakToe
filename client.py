from socket import *
#from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from tools import InputAdress
import time
from OtoPy import UsefulTools
import atexit

oLogger = UsefulTools.OLogger(logStreamLevel="DEBUG")

class ClientSocketHandler():

    def __init__(self):
        self.SERVER_ADDR = InputAdress()
        self.ENCODE_FORMAT = "utf-8"
        self.DISCONECT_MESSAGE = "!DISCONNECT"
        self.HANDLE_CONNECTION = True
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.responseListenerThread = Thread(target=self.ResponseListener, daemon=True)     
    
    def ConnectServer(self):
        try:
            self.clientSocket.connect(self.SERVER_ADDR)
            oLogger.LogWarning("Connected to Server!")
            return True
        except ConnectionRefusedError:
            oLogger.LogError(f"Fail to connect to adress: {self.SERVER_ADDR}")
            oLogger.LogExceptError("One Error has occured trying to connect to the server")
            return False
        except:
            oLogger.LogExceptError("Some random error has occured")
            return False


    def SendMessage(self, message):
        if message != self.DISCONECT_MESSAGE:
            oLogger.LogInfo(f"[SEND] - Sending the message: {message} to the server")
            self.clientSocket.send(message.encode(self.ENCODE_FORMAT))
        else:
            self.CloseSocket()

    def ResponseListener(self):
        while self.HANDLE_CONNECTION:
            recivedMessage = self.clientSocket.recv(2048).decode(self.ENCODE_FORMAT).split("#")

            if recivedMessage[0] == "202":
                oLogger.LogInfo(recivedMessage)
            elif recivedMessage[0] == "210":
                oLogger.LogInfo(recivedMessage)
            elif recivedMessage[0] == "1006":
                self.HANDLE_CONNECTION = False
                
        exit()

    def StartSocket(self):
        oLogger.LogWarning("Starting Client...")
        if self.ConnectServer():
            self.responseListenerThread.start()
            while self.HANDLE_CONNECTION:
                message = input("Enter your message: ")
                self.SendMessage(message)
                time.sleep(0.1)
    
    def CloseSocket(self):
        oLogger.LogWarning("Closing forcely the connection...")
        self.clientSocket.send(conn.DISCONECT_MESSAGE.encode(self.ENCODE_FORMAT))
        self.responseListenerThread.join()
        oLogger.LogWarning("Connection Closed")

conn = ClientSocketHandler()
atexit.register(conn.CloseSocket)

conn.StartSocket()