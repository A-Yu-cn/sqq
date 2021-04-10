import json
import socket
from threading import Thread


def recv(c):
    while True:
        print(c.recv(4096).decode())


# hanxu
token = "92e5352dfae25bed36efa18db987d38e7fb989530a02656a2e319616690138af"


def wrap_message(mes):
    return json.dumps({
        'Authorization': token,
        # Pikachu
        'to': '99472',
        'content': mes
    }).encode()


client = socket.socket()

client.connect(('sqq.12138.site', 12345))
client.sendall(json.dumps({
    "Authorization": token
}).encode())

t = Thread(target=recv, args=(client,))
t.start()

while True:
    client.sendall(wrap_message(input(">>>")))
