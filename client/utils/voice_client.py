import json
import socket
from threading import Thread
import logging
from globalFile import GlobalData

import pyaudio

logging.getLogger(__name__)
logging.basicConfig(level='INFO')

global_data = GlobalData()


class VoiceClient(object):

    def __init__(self):
        self.voice_server_socket = global_data.voice_server_socket
        self.server_socket = global_data.socket_address
        self.client = socket.socket()
        self.authorization = {
            'Authorization': global_data.token
        }
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 10000
        self.p = pyaudio.PyAudio()
        self.play_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                       frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

    def start_voice(self):
        # 开始语音通话过程
        self.voice_client = socket.socket()
        self.voice_client.connect(self.voice_server_socket)
        self.voice_client.sendall(json.dumps(self.authorization).encode())
        self.voice_client.recv(1024)
        # 开启语音监听线程和发送线程
        Thread(target=self.voice_listener).start()
        Thread(target=self.voice_sender).start()

    def voice_sender(self):
        """语音发送"""
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.voice_client.sendall(data)
            except:
                self.voice_client = None
                logging.info('disconnect')
                break

    def voice_listener(self):
        """语音监听"""
        logging.info('voice listener start listening')
        while True:
            try:
                data = self.voice_client.recv(1024)
                self.play_stream.write(data)
            except:
                self.voice_client = None
                logging.info('disconnect')
                break

    def run(self):
        self.start_voice()
