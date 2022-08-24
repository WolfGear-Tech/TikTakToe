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

        self.__CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
        self.__DISCONECT_MESSAGE = {"message": "!DISCONNECT"}
        self.__KEEP_ALIVE = {"message": "!KEEP_ALIVE"}
        self.__CONNECTION_STATE = False
        self.__readyToSendDataQueue = []
        self.__recivedDataQueue = []  
        self.__safeToWriteSendQueue = True
        self.__safeToWriteReciveQueue = True
    
    def __Connect(self) -> bool:
        try:
            self.__CLIENT_SOCKET.connect(self.SERVER_ADDR)
            self.oLogger.LogWarning("Connected to Server!")
            return True
        except ConnectionRefusedError:
            self.oLogger.LogError(f"Fail to connect to adress: {self.SERVER_ADDR}")
            return False
        except Exception:
            self.oLogger.LogExceptError("Some error has occured")
            return False

    def __EncodeAndSendData(self, data: dict[str: any]) -> None:
        data.update(self.USER)
        encodedData = base64.b64encode(bytes(str(data),'utf-8'))
        self.__CLIENT_SOCKET.send(encodedData)

    def __SendQueuedData(self) -> None:
        while not self.__safeToWriteSendQueue: 
            ... #Wait to Write on Shared variable
        if bool(self.__readyToSendDataQueue):
            self.__safeToWriteSendQueue = False
            self.__EncodeAndSendData(self.__readyToSendDataQueue.pop(0))
            self.__safeToWriteSendQueue = True
        else:
            self.__EncodeAndSendData(self.__KEEP_ALIVE)
    
    def __ReciveAndDecodedData(self) -> dict:
        clientSocketResponse = self.__CLIENT_SOCKET.recv(2048)
        if not clientSocketResponse == b'':
            responseList = base64.b64decode(clientSocketResponse).decode(self.ENCODE_FORMAT).replace("'",'"').replace("}{", "}&{").split("&")            
            decodedDictList = []
            for response in responseList:
                decodedDictList.append(json.loads(response))
            self.oLogger.LogDebug(f"Income Data DICT LIST: {decodedDictList}")
            return decodedDictList
        return [{"status": 204}]

    def __MessageHandler(self, status: int, data: dict) -> None:
            message = data.get("message", None)

            if status == 202:
                self.oLogger.LogInfo(message)
            elif status == 210:
                self.oLogger.LogInfo(message)
                while not self.__safeToWriteReciveQueue: 
                    ... #Wait to Write on Shared variable
                self.__safeToWriteSendQueue = False
                self.__recivedDataQueue.append(data)
                self.oLogger.LogDebug(f"The new Recievment was appended <{data}>")
                self.__safeToWriteSendQueue = True

    def __ClientHandler_Thread(self) -> None:
        try:
            while self.__CONNECTION_STATE:
                self.__SendQueuedData()
                responseList = self.__ReciveAndDecodedData()
                for response in responseList:
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

    def SendData(self, **data: dict[str: any]) -> bool:
        if bool(data):
            self.oLogger.LogWarning(data)
            if self.__CONNECTION_STATE:
                while not self.__safeToWriteSendQueue: 
                    ...
                self.__safeToWriteSendQueue = False
                self.__readyToSendDataQueue.append(data)
                self.oLogger.LogDebug(conn.__readyToSendDataQueue)
                self.__safeToWriteSendQueue = True
                return True
        return False

    def GetQueuedData(self) -> list:
        if bool(self.__recivedDataQueue):
            while not self.__safeToWriteReciveQueue: 
                    ... #Wait to Write on Shared variable
            self.__safeToWriteSendQueue = False
            dataInQueue = self.__recivedDataQueue
            self.__recivedDataQueue = []
            self.__safeToWriteSendQueue = True
            return dataInQueue

        return []

    def StartSocket(self) -> bool:
        if not self.__CONNECTION_STATE:
            self.oLogger.LogWarning("Starting Client...")
            if self.__Connect():
                self.__CONNECTION_STATE = True
                Thread(target=self.__ClientHandler_Thread, daemon=True).start()
                return True

        else:
            self.oLogger.LogWarning("Socket Already Started")
        return False
    
    def StopSocket(self) -> bool:
        if self.__CONNECTION_STATE:
            self.oLogger.LogWarning("Closing the connection...")
            self.__CONNECTION_STATE = False
            self.__EncodeAndSendData(self.__DISCONECT_MESSAGE)
            self.oLogger.LogWarning("Connection Closed.")
            return True

        return False

if __name__ == "__main__":
    conn = ClientSocketHandler("172.81.60.73", 8090, "Other", logOnTerminal=True, logLevel="DEBUG")
    print(conn.StartSocket())
    print(conn.SendData(message="delta"))
    for index in range(1, 60):
        print(conn.SendData(message=str(index + 600)))
    time.sleep(12)
    print(conn.GetQueuedData())
    print(conn.StopSocket())
    time.sleep(5)