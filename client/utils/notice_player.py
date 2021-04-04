from threading import Thread
from globalFile import GlobalData
import pyaudio
import base64


class NoticePlayer(Thread):

    def __init__(self):
        super(NoticePlayer, self).__init__()
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 32000
        self.p = pyaudio.PyAudio()
        self.global_data = GlobalData()
        with open('media/notice', 'r') as f:
            self.notice = base64.b64decode(f.read())

    def run(self):
        while True:
            notice = self.global_data.notice_queue.get()
            play_stream = self.p.open(format=self.audio_format, channels=self.channels,
                                      rate=self.rate, output=True,
                                      frames_per_buffer=self.chunk_size)
            play_stream.write(self.notice)
            play_stream.close()
