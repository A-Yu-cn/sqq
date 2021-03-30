from threading import Thread
from win10toast import ToastNotifier
from golbalFile import GlobalData

toaster = ToastNotifier()
globalData = GlobalData()


class ToasterSender(Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        # 清空消息队列
        while True:
            toaster.show_toast('消息提示', globalData.toast_message_queue.get())
