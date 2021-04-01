from threading import Thread
from win10toast import ToastNotifier
from globalFile import GlobalData
from utils.notice_sender import NotificationWindow

toaster = ToastNotifier()
global_data = GlobalData()


class ToasterSender(Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        # 清空消息队列
        while True:
            # toaster.show_toast('消息提示', global_data.toast_message_queue.get())
            NotificationWindow.info("消息提示", global_data.toast_message_queue.get())
