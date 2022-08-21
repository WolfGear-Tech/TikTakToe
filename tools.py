import re
from socket import gethostbyname
import json
import base64

def InputAdress():
    DEFAULT_ADDR = "otoma.solutions"
    DEFAULT_PORT = 8090
    adress = input(f"Digite o endereço IP ou DNS do servidor [{DEFAULT_ADDR}]: ") or DEFAULT_ADDR
    adressIP = ParseAdress(adress)
    port = int(input(f"Digite a porta do servidor [8090]: ") or DEFAULT_PORT)
    return (adressIP, port)

def ParseAdress(adress):
    isIP = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", adress)
    adressIP = adress if isIP else gethostbyname(adress)
    return adressIP

def EncodeMensage(status, user, mensage):
    dict = {"status": status, "user": user, "mensage": mensage}
    encoded_mensage = base64.b64encode(bytes(str(dict),'utf-8'))
    return encoded_mensage

def DecodeMensage(mensage):
    decoded_mensage = json.loads(base64.b64decode(mensage).decode('utf-8').replace("'",'"'))
    return decoded_mensage
