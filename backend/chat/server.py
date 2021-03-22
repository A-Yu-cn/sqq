import socket
import json
from threading import Thread
from chat.models import *
from django.utils import timezone
import logging

# 设置日志等级和格式
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s]  %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p')

# 客户端连接池
client_pool = {}


def send_message(user, message):
    if user.id in client_pool:
        client_pool[user.id].sendall(wrap_message(message))
    else:
        unread_message = UnreadMessage(user=user, message=message)
        unread_message.save()


def wrap_message(message):
    return json.dumps({
        'from': message.from_user.id,
        'to': message.to,
        'content': message.content,
        'time': timezone.localtime(message.createTime).isoformat()
    }).encode()


def wrap_error_data(mes):
    return json.dumps({
        'mes': mes
    }).encode()


class Receiver(Thread):

    def __init__(self, client, user_id, *args, **kwargs):
        super(Receiver, self).__init__(*args, **kwargs)
        self.client = client
        self.user_id = user_id

    def run(self):
        while True:
            try:
                data = json.loads(self.client.recv(4096))
                token = Token.objects.get(content=data.get('Authorization'))
                to = int(data.get('to'))
                message = Message(from_user=token.user, to=to, content=data.get('content'),
                                  createTime=timezone.now())
                message.save()
                # 用户id小于100000
                if to < 100000:
                    send_message(User.objects.get(id=to), message)
                else:
                    chatroom = Chatroom.objects.get(id=to)
                    for user in chatroom.users.all():
                        # 群消息不发给自己
                        if user.id == token.user.id:
                            break
                        send_message(user, message)
            except json.decoder.JSONDecodeError:
                try:
                    self.client.sendall(wrap_error_data('json decode error'))
                except ConnectionAbortedError:
                    # 客户端断开连接
                    client_pool.pop(self.user_id)
                    logger.warning(f'User<{self.user_id}> disconnect')
                    break
            except Token.DoesNotExist:
                self.client.sendall(wrap_error_data('token error'))
            except User.DoesNotExist:
                self.client.sendall(wrap_error_data('wrong user id'))
            except ValueError:
                self.client.sendall(wrap_error_data("wrong destination"))
            except (ConnectionError, ConnectionAbortedError):
                # 客户端断开连接
                client_pool.pop(self.user_id)
                logger.warning(f'User<{self.user_id}> disconnect')
                break


class Server(Thread):

    def __init__(self):
        super(Server, self).__init__()
        self.port = 12345

    def run(self) -> None:
        global client_pool
        server = socket.socket()
        server.bind(('', self.port))
        server.listen(20)
        while True:
            client, addr = server.accept()
            try:
                data = json.loads(client.recv(4096))
                token = Token.objects.get(content=data.get('Authorization'))
                client_pool[token.user.id] = client
                client.sendall(json.dumps({"mes": "", "data": token.user.id}).encode())
                receiver = Receiver(client, token.user.id)
                receiver.start()
                logger.warning(f'User<{token.user.id}> connect from {addr}')
            except json.decoder.JSONDecodeError:
                client.close()
            except Token.DoesNotExist:
                client.close()


s = Server()
s.setDaemon(True)
s.start()
