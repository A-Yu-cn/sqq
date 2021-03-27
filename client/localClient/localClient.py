import json
import socket
from threading import Thread


# 客户端类
# 功能：发送、接受消息；添加好友、加入群聊等
class Client:
    def __init__(self, token, target):
        self.token = token
        self.target = target
        self.client = socket.socket()
        self.mes_data = ""

        self.client.connect(('sqq.12138.site', 12345))
        self.client.sendall(json.dumps({
            "Authorization": self.token
        }).encode())

        # t = Thread(target=self.recv, args=(self.client,))
        # t.start()

    # 封装消息
    def wrap_message(self, mes=""):
        return json.dumps({
            'Authorization': self.token,
            'to': self.target,
            'content': mes
        }).encode()

    # 接收消息
    def recv(self, c):
        while True:
            data = c.recv(4096).decode()
            if not data:
                print("连接断开")
                break
            print(json.loads(data))

    # 发送消息
    def sendMessage(self, mes=""):
        self.client.sendall(self.wrap_message(mes))

# c = Client("92e5352dfae25bed36efa18db987d38e7fb989530a02656a2e319616690138af", '36568')
# c.sendMessage('''666''')
