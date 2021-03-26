import json
import socket
from threading import Thread


def recv(c):
    while True:
        print(c.recv(4096).decode())


token = "3b17f323e22a750f443c65c656047444f69328bb8e80c1144ef922d2bcf31de5"


def wrap_message(mes):
    return json.dumps({
        'Authorization': token,
        'to': '42560',
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
