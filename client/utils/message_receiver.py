from golbalFile import GlobalData
from threading import Thread
import json
from utils import connect_server
from win10toast import ToastNotifier

global_data = GlobalData()
toaster = ToastNotifier()


class MessageReceiver(Thread):

    @property
    def message(self):
        res = b""
        while True:
            try:
                data = global_data.client.recv(global_data.recv_buff)
                if not data:
                    raise ConnectionError
                res += data
                res = json.loads(res)
                return res
            except json.decoder.JSONDecodeError:
                pass

    def run(self) -> None:
        while True:
            if global_data.client is not None:
                try:
                    message = self.message
                    if str(message.get('from').get('id')) == str(global_data.chat_user) or str(message.get('to')) == str(global_data.chat_user):
                        # TODO: 这里添加将消息显示到正在聊天的界面上
                        pass
                    else:
                        # 这里只做全局提示
                        toaster.show_toast('消息提示', f'收到来自{message.get("from").get("nickname")}的消息')
                except (ConnectionError, ConnectionResetError):
                    global_data.client = None
                except Exception:
                    global_data.client = None
            else:
                connect_server.connect()
