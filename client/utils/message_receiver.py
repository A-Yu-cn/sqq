from globalFile import GlobalData
from threading import Thread
import json
from utils import connect_server

global_data = GlobalData()


class MessageReceiver(Thread):

    @property
    def message(self):
        res = b""
        data = ""
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
                    message_recv = self.message
                    message_type = message_recv.get("type")
                    message = message_recv.get("data")
                    # 正常接收消息
                    if message_type == 0:
                        if str(message.get('from').get('id')) == str(global_data.chat_user) or str(
                                message.get('to')) == str(global_data.chat_user):
                            global_data.message_receive_queue.put(message)
                            # todo 消息提示音
                            global_data.notice_queue.put(1)
                        else:
                            # 这里只做全局提示
                            from_user = message.get('from').get('nickname')
                            if len(str(message.get('to'))) > 5:
                                global_data.toast_message_queue.put(f'收到群({message.get("to")})消息，来自{from_user}')
                            else:
                                global_data.toast_message_queue.put(f"收到来自{from_user}的消息")
                    # 被添加为好友
                    elif message_type == 1:
                        global_data.refresh_friend_list_single.put(1)
                    # 被某人删除好友
                    elif message_type == 2:
                        global_data.refresh_friend_list_single.put(2)
                    # 被拉进群聊
                    elif message_type == 3:
                        global_data.refresh_friend_list_single.put(3)
                    # 语音通话请求
                    elif message_type == 4:
                        global_data.mes_from_id = int(message_recv.get('from').get('id'))
                        global_data.mes_from_username = message_recv.get('from').get('nickname')
                        global_data.refresh_friend_list_single.put(4)
                    # 语音通话回复
                    elif message_type == 5:
                        global_data.message_receive_queue.put(message_recv)
                except (ConnectionError, ConnectionResetError):
                    global_data.client = None
                except Exception as e:
                    global_data.logger.error(e)
                    global_data.client = None
            else:
                connect_server.connect()
