import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from globalFile import GlobalData
from voice_call.voiceCall import Ui_Form
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer

global_data = GlobalData()


class VoicePhoneWindow(QMainWindow, Ui_Form):

    def __init__(self, loginInfo):
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
        self.loginInfo = loginInfo
        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time)

    def time(self):
        self.label_2.setText('{} s'.format(time.time()))

    # 开始语音通话
    def startVoicePhone(self):
        self.timer.start(2 * 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = VoicePhoneWindow({})

    myWin.show()

    sys.exit(app.exec_())
