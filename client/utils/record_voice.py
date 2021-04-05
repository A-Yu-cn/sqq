import pyaudio
import wave
from globalFile import GlobalData
from threading import Thread

globalData = GlobalData()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 50  # 需要录制的时间
WAVE_OUTPUT_FILENAME = "output.wav"  # 保存的文件名


class Recorder(Thread):

    # 开始录音
    def start_record(self):
        globalData.record_signal = True
        p = pyaudio.PyAudio()  # 初始化
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # 创建录音文件
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if globalData.record_signal is False:
                break
            data = stream.read(CHUNK)
            frames.append(data)  # 开始录音

        stream.stop_stream()
        stream.close()
        p.terminate()
        globalData.record_queue.put(b''.join(frames))

    def run(self) -> None:
        self.start_record()
