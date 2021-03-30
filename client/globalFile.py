import queue
import logging


class GlobalData(object):
    __instance = None
    base_url = "https://sqq.12138.site:1234"
    client = None
    proxies = {
        'http': None,
        'https': None
    }
    self_data = None
    token = ''
    message_sender_queue = queue.Queue()
    socket_address = ('sqq.12138.site', 12345)
    recv_buff = 4096
    logger = logging.getLogger()
    chat_user = 0
    log_file = ''
    message_receive_queue = queue.Queue()
    toast_message_queue = queue.Queue()

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
