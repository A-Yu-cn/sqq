import json
import socket
from threading import Thread


# 客户端类
# 功能：发送、接受消息；添加好友、加入群聊等
class Client:
    def __init__(self):
        self.token = ""
        self.client = socket.socket()

        self.client.connect(('sqq.12138.site', 12345))
        self.client.sendall(json.dumps({
            "Authorization": self.token
        }).encode())

        t = Thread(target=self.recv, args=(self.client,))
        t.start()

    # 封装消息
    def wrap_message(self, mes=""):
        return json.dumps({
            'Authorization': self.token,
            'to': '36568',
            'content': mes
        }).encode()

    # 接收消息
    def recv(self, c):
        while True:
            print(c.recv(4096).decode())
