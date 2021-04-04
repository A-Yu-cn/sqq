from globalFile import GlobalData
from threading import Thread
import json
from utils import connect_server
import winsound
import pyaudio
import base64

global_data = GlobalData()


class MessageReceiver(Thread):

    def __init__(self):
        super(MessageReceiver, self).__init__()
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 32000
        self.p = pyaudio.PyAudio()
        with open('media/notice', 'r') as f:
            self.notice = base64.b64decode(f.read())

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
                    message_type = message.get("type")
                    message = message.get("data")
                    # 正常接收消息
                    if message_type == 0:
                        if str(message.get('from').get('id')) == str(global_data.chat_user) or str(
                                message.get('to')) == str(global_data.chat_user):
                            global_data.message_receive_queue.put(message)
                            # todo 消息提示音
                            self.play_stream = self.p.open(format=self.audio_format, channels=self.channels,
                                                           rate=self.rate, output=True,
                                                           frames_per_buffer=self.chunk_size)
                            self.play_stream.write(self.notice)
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
                except (ConnectionError, ConnectionResetError):
                    global_data.client = None
                except Exception as e:
                    global_data.logger.error(e)
                    global_data.client = None
            else:
                connect_server.connect()
