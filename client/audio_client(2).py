import socket
import logging
from threading import Thread
import pyaudio


class Client(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='[%(asctime)s]  %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p', level='INFO')
        self.client = socket.socket()
        self.server_socket = ('222.28.41.215', 1024)
        self.client.connect(self.server_socket)
        Thread(target=self.listener).start()
        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 10000
        self.p = pyaudio.PyAudio()
        self.play_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                       frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

    def listener(self):
        self.logger.info('start listening')
        while True:
            data = self.client.recv(1024)
            self.logger.info("recv")
            self.play_stream.write(data)

    def sender(self):
        while True:
            data = self.recording_stream.read(1024)
            self.logger.info("sending...")
            self.client.sendall(data)


client = Client()
client.sender()
