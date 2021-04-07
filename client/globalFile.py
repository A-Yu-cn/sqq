import queue
import logging
import pyaudio


class GlobalData(object):
    __instance = None
    base_url = "https://sqq.12138.site:1234"
    client = None
    voice_client = None
    proxies = {
        'http': None,
        'https': None
    }
    self_data = None
    token = ''
    message_sender_queue = queue.Queue()
    socket_address = ('sqq.12138.site', 12345)
    voice_server_socket = ('sqq.12138.site', 23456)
    recv_buff = 4096
    logger = logging.getLogger()
    chat_user = 0
    log_file = ''
    message_receive_queue = queue.Queue()
    toast_message_queue = queue.Queue()
    db_file_path = "sqq.db"
    record_signal = False  # 语音录制信号
    record_queue = queue.Queue()  # 语音队列
    refresh_friend_list_single = queue.Queue()
    notice_queue = queue.Queue()  # 消息提示队列
    mes_from_id = 0  # 语音通话用户请求id
    mes_from_username = ""  # 语音通话用户请求用户名
    voice_params = {"frames_per_buffer": 1024,
                    "format": pyaudio.paInt16,
                    "channels": 1,
                    "rate": 10000}
    is_calling = False

    def __init__(self):
        if self.log_file:
            logging.basicConfig(filename=self.log_file, format='[%(asctime)s]  %(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S %p', level='INFO')
        else:
            logging.basicConfig(format='[%(asctime)s]  %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p', level='INFO')

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
