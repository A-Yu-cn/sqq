from threading import Thread
from globalFile import GlobalData
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

    @staticmethod
    def __wrap_voice_response_message(response):
        # 发送语音通话回复请求
        return json.dumps({
            "type": 1,
            "from_id": global_data.mes_from_id,
            "response": response,
        }).encode()

    @staticmethod
    def __wrap_voice_request_message(to_id):
        # 发送语音通话请求
        return json.dumps({
            "type": 0,
            "user_id": to_id
        }).encode()

    def run(self) -> None:
        while True:
            if global_data.client is not None:
                try:
                    mes = global_data.message_sender_queue.get()
                    if mes['type_'] == 0:  # 普通消息
                        to = mes['data']['chatNumber']
                        content = mes['data']['content']
                        global_data.client.sendall(self.__wrap_message(to, content))
                        global_data.logger.info(f'向{to}发送消息成功')
                    elif mes['type_'] == 1:  # 语音回复消息
                        response = mes['response']
                        global_data.client.sendall(self.__wrap_voice_response_message(response))
                    elif mes["type_"] == 2:  # 语音请求消息
                        to_id = mes['to_id']
                        global_data.client.sendall(self.__wrap_voice_request_message(to_id))
                    # 阻塞获取消息完成之后连接可能断掉
                    if global_data.client is None:
                        global_data.client = None
                        continue
                except Exception:
                    global_data.client = None
