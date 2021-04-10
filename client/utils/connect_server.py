from globalFile import GlobalData
import socket
import json

global_data = GlobalData()


def connect():
    global_data.client = socket.socket()
    global_data.client.connect(global_data.socket_address)
    global_data.client.sendall(json.dumps({
        'Authorization': global_data.token
    }).encode())
    global_data.client.settimeout(1)
    try:
        if not json.loads(global_data.client.recv(4096)).get('mes'):
            global_data.logger.info('连接服务器成功')
            global_data.client.settimeout(None)
        else:
            global_data.client = None
            global_data.logger.warning('连接服务器失败')
    except socket.timeout:
        # 连接超时
        global_data.client = None
        global_data.logger.warning('连接服务器失败')
