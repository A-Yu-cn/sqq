from threading import Thread
from globalFile import GlobalData
import json
import pyaudio

global_data = GlobalData()


class VoiceSender(Thread):
    def run(self):
        p = pyaudio.PyAudio()
        recording_stream = p.open(**global_data.voice_params, input=True)
        """语音发送"""
        while True:
            try:
                data = recording_stream.read(1024)
                global_data.voice_client.sendall(data)
            except Exception as e:
                global_data.logger.info('sender:disconnect from voice server.')
                break
        # todo 提示断开连接
