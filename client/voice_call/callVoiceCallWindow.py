import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from globalFile import GlobalData
from voice_call.voiceCall import Ui_Form
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from utils.start_voice_server import start_voice
from utils.notice_sender import NotificationWindow

global_data = GlobalData()


class Listener(QThread):
    signal = pyqtSignal(object)

    def run(self) -> None:
        while True:
            time.sleep(0.5)
            if global_data.is_calling:
                continue
            self.signal.emit(1)
            break


class VoicePhoneWindow(QMainWindow, Ui_Form):

    def __init__(self):
        super(VoicePhoneWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("语音通话")
        self.setWindowIcon(QtGui.QIcon('imgs/phone.png'))
        self.setStyleSheet('''
        QPushButton{
            border-radius: 50px;
            border-style: outset;
            background: red;
            border-image: url(imgs/phone.png);
            }
        QPushButton:hover{
            border-radius: 50px;
            border-style: outset;
            background-color: #ff5964;
            border-image: url(imgs/phone.png);
            }
        QWidget#Form{
            background-color: lightgrey;
            }
        ''')
        if global_data.mes_from_username:
            self.label.setText(global_data.mes_from_username[0])
        else:
            self.label.setText(global_data.chat_user_name[0])
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.showTime)
        self.pushButton.clicked.connect(self.stopVoicePhone)
        self.time_text = 0
        global_data.is_calling = True
        self.listener = Listener()
        self.listener.signal.connect(self.stopVoicePhone)
        self.listener.start()
        self.startVoicePhone()  # 打开界面即开始通话

    # 改变时间显示
    def showTime(self):
        # 在标签上显示时间
        self.time_text += 1
        self.label_2.setText(str(self.transform_time(self.time_text)))

    # 转时分秒
    def transform_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timestr = "%02d:%02d:%02d" % (h, m, s)
        return timestr

    # 开始通话
    def startVoicePhone(self):
        self.timer.start(1000)
        start_voice()

    # 结束通话
    def stopVoicePhone(self, type_=0):
        global_data.mes_from_id = 0
        global_data.mes_from_username = ""
        try:
            self.timer.stop()
            global_data.voice_client.close()
        except Exception as e:
            global_data.logger.error(e)
        self.destroy()
        if type_ == 1:
            NotificationWindow.info("提示", "通话已断开")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = VoicePhoneWindow()

    myWin.show()

    sys.exit(app.exec_())
