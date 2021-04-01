import socket
import json
from threading import Thread
from chat.models import *
from django.utils import timezone
import logging
import os

# 设置日志等级和格式
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s]  %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p')

# 客户端连接池
client_pool = {}


def send_message(user, message, type_=0):
    """向指定用户发送消息"""
    if type_ == 0:
        # 发送聊天消息
        if user.id in client_pool:
            client_pool[user.id].sendall(wrap_message(message))
        else:
            # 记录未读消息
            unread_message = UnreadMessage(user=user, message=message)
            unread_message.save()
    elif type_ == 1:
        if user.id in client_pool and isinstance(message, User):
            # 被某人添加为好友
            client_pool[user.id].sendall(json.dumps({
                'type': 1,
                'data': {
                    'id': message.id,
                    'nickname': message.nickname
                }
            }).encode())
    elif type_ == 2:
        # 被某人删除好友
        if user.id in client_pool and isinstance(message, User):
            client_pool[user.id].sendall(json.dumps({
                'type': 2,
                'data': {
                    'id': message.id,
                    'nickname': message.nickname
                }
            }).encode())
    elif type_ == 3:
        # 被某人拉进群聊
        if user.id in client_pool and isinstance(message, Chatroom):
            client_pool[user.id].sendall(json.dumps({
                'type': 3,
                'data': {
                    'id': message.id,
                    'name': message.name
                }
            }).encode())


def wrap_message(message):
    """包装向客户发送的消息"""
    return json.dumps({
        'type': 0,
        'data': {
            'from': {
                'id': message.from_user.id,
                'nickname': message.from_user.nickname
            },
            'to': message.to,
            'content': message.content,
            'time': timezone.localtime(message.createTime).isoformat()
        }
    }).encode()


def wrap_error_data(mes):
    """包装错误消息"""
    return json.dumps({
        'mes': mes
    }).encode()


class Receiver(Thread):

    def __init__(self, client, user_id, *args, **kwargs):
        super(Receiver, self).__init__(*args, **kwargs)
        self.client = client
        self.client.settimeout(int(os.environ.get('RECV_TIME_OUT')))  # 接受消息超时
        self.user_id = user_id
        self.recv_buff = int(os.environ.get('TCP_RECV_BUFF'))  # 接受缓冲区

    def recv_message(self):
        """接受一个完整的消息"""
        res = b""
        while True:
            try:
                res += self.client.recv(self.recv_buff)
                res = json.loads(res)
                return res
            except json.decoder.JSONDecodeError:
                pass

    def run(self):
        while True:
            try:
                data = self.recv_message()
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
                            continue
                        send_message(user, message)
            except json.decoder.JSONDecodeError:
                try:
                    self.client.sendall(wrap_error_data('json decode error'))
                except ConnectionAbortedError:
                    # 客户端断开连接
                    self.client.close()
                    client_pool.pop(self.user_id)
                    logger.warning(f'User<{self.user_id}> disconnect')
                    break
            except Token.DoesNotExist:
                self.client.sendall(wrap_error_data('token error'))
            except User.DoesNotExist:
                self.client.sendall(wrap_error_data('wrong user id'))
            except ValueError:
                self.client.sendall(wrap_error_data("wrong destination"))
            except (ConnectionError, ConnectionAbortedError, ConnectionResetError):
                # 客户端断开连接
                self.client.close()
                client_pool.pop(self.user_id)
                logger.warning(f'User<{self.user_id}> disconnect')
                break
            except socket.timeout:
                self.client.close()
                client_pool.pop(self.user_id)
                logger.warning(f'User<{self.user_id}> time out')
            except Exception as e:
                self.client.close()
                logger.error(e)
                break


class Server(Thread):

    def __init__(self):
        super(Server, self).__init__()
        self.port = int(os.environ.get('TCP_SERVER_PORT'))

    def run(self) -> None:
        global client_pool
        server = socket.socket()
        server.bind(('', self.port))
        server.listen(20)
        logger.warning(f'bind {self.port}, start listening...')
        while True:
            client, addr = server.accept()
            try:
                logging.warning(f'connecting from {addr}')
                client.settimeout(3)
                data = json.loads(client.recv(4096))
                client.settimeout(None)
                token = Token.objects.get(content=data.get('Authorization'))
                client_pool[token.user.id] = client
                client.sendall(json.dumps({"mes": "", "data": token.user.id}).encode())
                receiver = Receiver(client, token.user.id)
                receiver.start()
                logger.warning(f'User<{token.user.id}> connect from {addr}')
            except json.decoder.JSONDecodeError:
                client.sendall(wrap_error_data('wrong data type'))
                client.close()
            except Token.DoesNotExist:
                client.sendall(wrap_error_data('wrong token'))
                client.close()
            except socket.timeout:
                logger.warning(f'{addr} time out')
                client.sendall(wrap_error_data('time out'))
                client.close()
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                client.close()
            except Exception as e:
                logger.warning(e)


s = Server()
s.setDaemon(True)
s.start()
