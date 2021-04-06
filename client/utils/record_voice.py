import pyaudio
import wave
from globalFile import GlobalData
from threading import Thread
import base64

globalData = GlobalData()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
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
        # globalData.record_queue.put(b''.join(frames))
        # 保存wav录音文件再转换base64
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 保存
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        globalData.record_queue.put(self.toBase64(WAVE_OUTPUT_FILENAME))
        # wf.close()

    def toBase64(self, file):
        with open(file, 'rb') as fileObj:
            audio_data = fileObj.read()
            base64_data = base64.b64encode(audio_data)
            print(base64_data)
            return base64_data

    def run(self) -> None:
        self.start_record()
