from globalFile import GlobalData
from threading import Thread
import json
from utils import connect_server
import winsound

global_data = GlobalData()


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
                    message_type = message.get("type")
                    message = self.message.get("data")
                    # 正常接收消息
                    if message_type == 0:
                        if str(message.get('from').get('id')) == str(global_data.chat_user) or str(
                                message.get('to')) == str(global_data.chat_user):
                            global_data.message_receive_queue.put(message)
                            # todo 消息提示音
                        else:
                            # 这里只做全局提示
                            from_user = message.get('from').get('nickname')
                            if len(str(message.get('to'))) > 5:
                                global_data.toast_message_queue.put(f'收到群({message.get("to")})消息，来自{from_user}')
                            else:
                                global_data.toast_message_queue.put(f"收到来自{from_user}的消息")
                    # 被添加为好友
                    elif message_type == 1:
                        pass
                    # 被某人删除好友
                    elif message_type == 2:
                        pass
                    # 被拉进群聊
                    elif message_type == 3:
                        pass
                except (ConnectionError, ConnectionResetError):
                    global_data.client = None
                except Exception:
                    global_data.client = None
            else:
                connect_server.connect()
