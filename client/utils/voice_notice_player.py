import time

from globalFile import GlobalData
from threading import Thread

global_data = GlobalData()


class VoiceNoticePLayer(Thread):

    def run(self) -> None:
        while True:
            if global_data.is_voice_notice:
                global_data.notice_queue.put(2)
                time.sleep(1)
            else:
                break
