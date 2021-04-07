from globalFile import GlobalData
import socket
import json
from threading import Thread
from utils.voice_sender import VoiceSender
from utils.voice_receiver import VoiceReceiver

global_data = GlobalData()


def start_voice():
    # 开始语音通话过程
    global_data.voice_client = socket.socket()
    global_data.voice_client.connect(global_data.voice_server_socket)
    global_data.voice_client.sendall(json.dumps({
        "Authorization": global_data.token
    }).encode())
    global_data.voice_client.recv(1024)
    # 开启语音监听线程和发送线程
    VoiceSender().start()
    VoiceReceiver().start()
