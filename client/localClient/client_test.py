import json
import socket
from threading import Thread


def recv(c):
    while True:
        print(c.recv(4096).decode())


token = "e8921h9h9898189921e9deh91hed912eh9128h9"


def wrap_message(mes):
    return json.dumps({
        'Authorization': token,
        'to': '36568',
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
