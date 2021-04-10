from threading import Thread
from globalFile import GlobalData
import json
import pyaudio

global_data = GlobalData()


class VoiceReceiver(Thread):
    def run(self):
        p = pyaudio.PyAudio()
        play_stream = p.open(**global_data.voice_params, output=True)
        """语音发送"""
        while True:
            try:
                data = global_data.voice_client.recv(1024)
                play_stream.write(data)
            except Exception as e:
                global_data.is_calling = False
                global_data.voice_client = None
                global_data.logger.info('disconnect from voice server.')
                global_data.logger.info('sender:disconnect from voice server.')
                break
        # todo 提示断开连接
