# 启动程序入口
import sys
from PyQt5.QtWidgets import QApplication

from loginWindow import callUserLogin

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = callUserLogin.UserLoginWindow()

    with open('css/userLogin.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
