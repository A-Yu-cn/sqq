"""
登录界面
"""
import json
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import requests

from loginWindow.userLogin import Ui_widget
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from listWindow.callListWindow import ListWindow
from registerWindow.callUserRegister import UserRegisterWindow
from forgetPasswordWindow.callForgetPasswordWindow import ResetPasswordWindow
from golbalFile import base_url


class UserLoginWindow(QMainWindow, Ui_widget):
    def __init__(self):
        super(UserLoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('../imgs/chat.png'))
        self.setWindowTitle('SQQ')
        # 待传递消息
        self.loginInfo = dict()
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 绑定登录事件
        self.loginButton.clicked.connect(self.userLogin)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.label_4.setAlignment(Qt.AlignCenter)
        # 图片加载
        jpg = QtGui.QPixmap("../imgs/logo2.png").scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(jpg)
        jpg = QtGui.QPixmap("../imgs/background.jpg").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        # 绑定注册事件
        self.registerButton.clicked.connect(self.userRegister)
        # 忘记密码
        self.forgetPasswordButton.clicked.connect(self.forgetPassword)

    # 用户登录
    def userLogin(self):
        if self.usernameLineEdit.text() == "":
            QMessageBox.warning(self, "警告", "请输入用户名！", QMessageBox.Yes)
        elif self.passwordLineEdit.text() == "":
            QMessageBox.warning(self, "警告", "请输入密码！", QMessageBox.Yes)
        else:
            username = str(self.usernameLineEdit.text())
            password = str(self.passwordLineEdit.text())
            res = self.checkLogin(username, password)
            # 登陆成功,一段时间后跳转
            if res is True:
                self.loginButton.setText("登陆成功，请稍后...")
                self.main_ui = ListWindow(self.loginInfo)
                # 加载样式
                with open('../css/listWindow.css') as file:
                    qss = file.readlines()
                    qss = ''.join(qss).strip('\n')
                self.main_ui.setStyleSheet(qss)
                self.main_ui.show()
                self.destroy()
            else:
                QMessageBox.warning(self, "警告", "请检查用户名或密码！", QMessageBox.Yes)
                return

    # 验证登录
    def checkLogin(self, username, password):
        url = base_url + "/users/auth"
        loginData = {"identity": username, "password": password}
        r = requests.post(url=url, json=loginData)
        # 登录错误
        if r.status_code == 500:
            return False
        elif json.loads(r.text)['mes'] == "":
            self.loginInfo = json.loads(r.text)
            print(self.loginInfo)
            return True
        else:
            return False

    # 用户注册
    def userRegister(self):
        self.regWindow = UserRegisterWindow()
        # 加载样式
        with open('../css/userRegister.css') as file:
            qss = file.readlines()
            qss = ''.join(qss).strip('\n')
        self.regWindow.setStyleSheet(qss)
        self.regWindow.show()

    # 忘记密码
    def forgetPassword(self):
        """忘记密码"""
        self.regWindow = ResetPasswordWindow()
        # 加载样式
        with open('../css/forgetWindow.css') as file:
            qss = file.readlines()
            qss = ''.join(qss).strip('\n')
        self.regWindow.setStyleSheet(qss)
        self.regWindow.show()


def start():
    app = QApplication(sys.argv)

    myWin = UserLoginWindow()

    with open('../css/userLogin.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = UserLoginWindow()

    with open('../css/userLogin.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
