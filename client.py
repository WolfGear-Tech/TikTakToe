from logging.handlers import SocketHandler
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from OtoPy import UsefulTools
import time
import json
import base64

class ClientSocketHandler():
    oLogger = None

    def __init__(self, adress, port, userName, **logSettings):
        self.oLogger = UsefulTools.OLogger(
            streamLogging=logSettings.get("logOnTerminal", False), 
            logStreamLevel=logSettings.get("logLevel", "NOTSET"),
        )

        self.SERVER_ADDR = (adress, port)
        self.USER = {"user": {"name" : userName}}
        self.ENCODE_FORMAT = "utf-8"
        self.DISCONECT_MESSAGE = {"message": "!DISCONNECT"}
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        self.__CONNECTION_STATE = False
        self.__readyToSendDataQueue = []
        self.__recivedDataQueue = []  
        self.__safeToWrite = True
    
    def __Connect(self) -> bool:
        try:
            self.clientSocket.connect(self.SERVER_ADDR)
            self.oLogger.LogWarning("Connected to Server!")
            return True
        except ConnectionRefusedError:
            self.oLogger.LogError(f"Fail to connect to adress: {self.SERVER_ADDR}")
            return False
        except Exception:
            self.oLogger.LogExceptError("Some error has occured")
            return False

    def __SendEncodedData(self, data: dict[str: any]) -> None:
        data.update(self.USER)
        encodedData = base64.b64encode(bytes(str(data),'utf-8'))
        self.clientSocket.send(encodedData)

    def __ReciveEncodedData(self) -> dict:
        clientSocketResponse = self.clientSocket.recv(2048)
        if not clientSocketResponse == b'':
            self.oLogger.LogDebug(f"ReceiveEncodedData clientSocketResponse: {clientSocketResponse}")
            decodedData = json.loads(base64.b64decode(clientSocketResponse).decode('utf-8').replace("'",'"'))
            return decodedData
        return {"status": 204}

    def __MessageHandler(self, status: int, data: dict) -> None:
            message = data.get("message", None)

            if status == 202:
                self.oLogger.LogInfo(message)
            elif status == 210:
                self.__recivedDataQueue.append(data)

    def __ClientListener_Thread(self) -> None:
        try:
            while self.__CONNECTION_STATE:
                response = self.__ReciveEncodedData()

                status = response.get("status", 500)
                if status in range(200, 300):
                    # Success
                    if not status == 204:
                        self.__MessageHandler(status, response)

                elif status in range(400, 500):
                    # Client Error
                    ...

                elif status in range(500, 9999):
                    # Server Error
                    self.StopSocket()

            exit()
        except ConnectionRefusedError:
            self.__CONNECTION_STATE = False
    
    def __HandleSend_Thread(self) -> None:
        while self.__CONNECTION_STATE:
            if self.__safeToWrite:
                self.__safeToWrite = False
                for data in self.__readyToSendDataQueue:
                    self.__SendEncodedData(data)
                    self.__readyToSendDataQueue.remove(data)
                    time.sleep(0.5)
                self.__safeToWrite = True

        exit()

    def SendData(self, **data: dict[str: any]) -> bool:
        if bool(data):
            self.oLogger.LogWarning(data)
            if self.__CONNECTION_STATE:
                while not self.__safeToWrite: ...
                self.__safeToWrite = False
                self.__readyToSendDataQueue.append(data)
                self.__safeToWrite = True
                return True
        return False

    def GetQueuedData(self) -> list:
        if len(self.__recivedDataQueue) > 0 and self.__CONNECTION_STATE:
            dataInQueue = self.__recivedDataQueue
            for data in self.__recivedDataQueue:
                if data in dataInQueue: self.__recivedDataQueue.remove(data)
            return dataInQueue

        return []

    def StartSocket(self) -> bool:
        if not self.__CONNECTION_STATE:
            self.oLogger.LogWarning("Starting Client...")
            if self.__Connect():
                self.__CONNECTION_STATE = True
                Thread(target=self.__ClientListener_Thread).start()
                Thread(target=self.__HandleSend_Thread).start()
                return True

        else:
            self.oLogger.LogWarning("Socket Already Started")
        return False
    
    def StopSocket(self) -> bool:
        if self.__CONNECTION_STATE:
            self.oLogger.LogWarning("Closing the connection...")
            self.__CONNECTION_STATE = False
            self.__SendEncodedData(self.DISCONECT_MESSAGE)
            self.oLogger.LogWarning("Connection Closed.")
            return True

        return False

conn = ClientSocketHandler("172.81.60.73", 8090, "Pstump", logOnTerminal=True, logLevel="DEBUG")
print(conn.StartSocket())
print(conn.SendData(message="delta"))
print(conn.SendData(message="0"))
print(conn.SendData(message="1"))
print(conn.SendData(message="2"))
print(conn.SendData(message="3"))
print(conn.SendData(message="4"))
print(conn.SendData(message="5"))
time.sleep(5)
print(conn.GetQueuedData())
print(conn.StopSocket())