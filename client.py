from socket import *
#from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
from threading import Thread
from tools import InputAdress, EncodeMessage, DecodeMessage
from OtoPy import UsefulTools
import atexit
import time

oLogger = UsefulTools.OLogger(logStreamLevel="DEBUG")

class ClientSocketHandler():

    def __init__(self):
        self.SERVER_ADDR = InputAdress()
        self.USER_NAME = input("Set a user name: ")
        self.ENCODE_FORMAT = "utf-8"
        self.DISCONECT_MESSAGE = "!DISCONNECT"
        self.HANDLE_CONNECTION = True
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.responseListenerThread = Thread(target=self.ResponseListener)     
    
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
            self.clientSocket.send(EncodeMessage(message=message, user={"name": self.USER_NAME}))
        else:
            self.CloseSocket()

    def ResponseListener(self):
        while self.HANDLE_CONNECTION:
            recivedDict = DecodeMessage(self.clientSocket.recv(2048))

            if recivedDict["status"] == 202:
                oLogger.LogInfo(recivedDict["message"])
            elif recivedDict["status"] == 210:
                oLogger.LogInfo(f"{recivedDict['user']}: {recivedDict['message']}")
            elif recivedDict["status"] == 1006:
                self.HANDLE_CONNECTION = False
                
        exit()

    def StartSocket(self):
        oLogger.LogWarning("Starting Client...")
        if self.ConnectServer():
            self.responseListenerThread.start()
            while self.HANDLE_CONNECTION:
                message = input("Enter your message: ")
                self.SendMessage(message)
                time.sleep(1)
    
    def CloseSocket(self):
        oLogger.LogWarning("Closing forcely the connection...")
        self.clientSocket.send(EncodeMessage(message=self.DISCONECT_MESSAGE))
        self.responseListenerThread.join()
        oLogger.LogWarning("Connection Closed")

conn = ClientSocketHandler()
atexit.register(conn.CloseSocket)

conn.StartSocket()