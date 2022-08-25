from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from OtoPy import UsefulTools
import time
import json
import base64

class ClientSocketHandler():
    oLogger = None

    def __init__(self, **logSettings):
        self.oLogger = UsefulTools.OLogger(
            streamLogging=logSettings.get("logOnTerminal", False), 
            logStreamLevel=logSettings.get("logLevel", "NOTSET"),
        )
        self.SERIAL = "QLY8LNU7FqR7LhRfEJmR"
        self.ENCODE_FORMAT = "utf-8"
        self.DISCONECT_RESPONSE = {"STATUS": 1006}
        self.DISCONECT_REQUEST = {"REQUEST_CODE": 1006}
        self.ECHO_REQUEST = {"REQUEST_CODE": 100}
        self.ECHO_RESPONSE = {"STATUS": 100}

        self.__CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
        self.__CONNECTION_STATE = False
        self.__readyToSendDataQueue = []
        self.__recivedDataQueue = []  
        self.__safeToWriteSendQueue = True
        self.__safeToWriteReciveQueue = True

    def __EncodeAndSendData(self, data: dict[str: any]) -> None:
        dataToSend = dict(self.ECHO_REQUEST)
        dataToSend.update(data)
        encodedData = base64.b64encode(bytes(str(dataToSend),'utf-8'))
        self.__CLIENT_SOCKET.send(encodedData)

    def __SendQueuedData(self) -> None:
        while not self.__safeToWriteSendQueue: 
            ... #Wait to Write on Shared variable
        if bool(self.__readyToSendDataQueue):
            self.__safeToWriteSendQueue = False
            self.__EncodeAndSendData(self.__readyToSendDataQueue.pop(0))
            self.__safeToWriteSendQueue = True
        else:
            self.__EncodeAndSendData(self.ECHO_REQUEST)
    
    def __ReciveAndDecodedData(self) -> dict:
        clientSocketResponse = self.__CLIENT_SOCKET.recv(2048)
        if not clientSocketResponse == b'':
            responseList = base64.b64decode(clientSocketResponse).decode(self.ENCODE_FORMAT).replace("'",'"').replace("}{", "}&{").split("&")            
            decodedDictList = []
            for response in responseList:
                decodedDictList.append(json.loads(response))
            return decodedDictList
        return [{"status": 100}]

    def __Connect(self, SERVER_ADDR) -> bool:
        try:
            print(self.__CLIENT_SOCKET.connect(SERVER_ADDR))
            self.oLogger.LogWarning("Connected to Server!")
            self.__EncodeAndSendData({"REQUEST_CODE": 101, "CRED": {"user": "!NO_USER", "password": "!NO_PASSWORD", "serial": self.SERIAL}})
            return True
        except ConnectionRefusedError:
            self.oLogger.LogError(f"Fail to connect to adress: {self.SERVER_ADDR}")
            return False
        except Exception:
            self.oLogger.LogExceptError("Some error has occured")
            return False

    def __AppendRecievedData(self, data):
        self.oLogger.LogInfo(data)
        while not self.__safeToWriteReciveQueue: 
            ... #Wait to Write on Shared variable
        self.__safeToWriteSendQueue = False
        self.__recivedDataQueue.append(data)
        self.oLogger.LogDebug(f"The new Recievment was appended <{data}>")
        self.__safeToWriteSendQueue = True

    def __DataHandler(self, data: dict) -> None:
        STATUS = data.get("STATUS", 500)
        if STATUS in range(100, 200):
            #Connection Stablisment
            if STATUS == 100: pass

            elif STATUS == 101: 
                ... #Login stuff

        elif STATUS in range(200, 300):
            # Success
            if STATUS == 202:
                pass #Data recived by server
                self.oLogger.LogDebug("Ok Response for data Recieved")

            elif STATUS == 205:
                #Data recieved from another user
                self.__AppendRecievedData(data)

            elif STATUS == 210:
                #Broadcast made by server from specific user
                self.__AppendRecievedData(data)

        elif STATUS in range(400, 500):
            # Client Error
            ...

        elif STATUS in range(500, 9999):
            # Server Error
            if STATUS == 1006:
                self.StopSocket()

    def __ClientHandler_Thread(self) -> None:
        try:
            while self.__CONNECTION_STATE:
                self.__SendQueuedData()
                responseList = self.__ReciveAndDecodedData()
                for response in responseList:
                    self.__DataHandler(response)
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
                self.oLogger.LogDebug(self.__readyToSendDataQueue)
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

    def StartSocket(self, serverAddres, serverPort) -> bool:
        SERVER_ADDR = (serverAddres, serverPort)

        if not self.__CONNECTION_STATE:
            self.oLogger.LogWarning("Starting Client...")
            if self.__Connect(SERVER_ADDR):
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
            self.__EncodeAndSendData(self.DISCONECT_REQUEST)
            self.oLogger.LogWarning("Connection Closed.")
            return True

        return False

if __name__ == "__main__":
    conn = ClientSocketHandler(logOnTerminal=True, logLevel="DEBUG")
    print(conn.StartSocket("192.168.1.252", 8090))
    for index in range(1, 60):
        print(conn.SendData(REQUEST_CODE = 205, numTest=str(index + 600)))
    print(conn.GetQueuedData())
    input()
    print(conn.GetQueuedData())
    input()
    conn.StopSocket()
    input()