from threading import Thread
from golbalFile import GlobalData
import json

global_data = GlobalData()


class MessageSender(Thread):

    @staticmethod
    def __wrap_message(to, content):
        return json.dumps({
            'Authorization': global_data.token,
            'to': to,
            'content': content
        }).encode()

    def run(self) -> None:
        while True:
            if global_data.client is not None:
                try:
                    to, content = global_data.message_sender_queue.get()
                    # 阻塞获取消息完成之后连接可能断掉
                    if global_data.client is None:
                        global_data.client = None
                        continue
                    global_data.client.sendall(self.__wrap_message(to, content))
                    global_data.logger.info(f'向{to}发送消息成功')
                except Exception:
                    global_data.client = None
