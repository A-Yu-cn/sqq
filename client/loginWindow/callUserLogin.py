"""
登录界面
"""
import configparser
import json
import sys
from PyQt5 import QtWidgets
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import requests

from loginWindow.userLogin import Ui_widget
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from listWindow.callListWindow import ListWindow
from registerWindow.callUserRegister import UserRegisterWindow
from forgetPasswordWindow.callForgetPasswordWindow import ResetPasswordWindow
from utils.message_sender import MessageSender
from utils.message_receiver import MessageReceiver
from utils import connect_server
from globalFile import GlobalData
from utils.toaster_sender import ToasterSender

global_data = GlobalData()


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
        ToasterSender().start()
        # 加载配置文件
        self.load_config()
        # 窗体样式
        # self.setWindowFlags(Qt.SubWindow)

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
        url = global_data.base_url + "/users/auth"
        loginData = {"identity": username, "password": password}
        r = requests.post(url=url, json=loginData, proxies=global_data.proxies)
        # 登录错误
        if r.status_code == 500:
            return False
        elif json.loads(r.text)['mes'] == "":
            # 登录成功事件
            self.loginInfo = json.loads(r.text)
            global_data.self_data = self.loginInfo.get('data').get('self')
            global_data.token = self.loginInfo.get('data').get('token')
            unread_message_usernames = list(set([message["from"][1] for message in
                                                 self.loginInfo.get('data').get('unread_message')]))
            for unread_mes_username in unread_message_usernames:
                global_data.toast_message_queue.put(f'有来自{unread_mes_username}的未读消息')
            config = configparser.ConfigParser()
            # 记住密码
            if self.checkBox_2.isChecked():
                config["DEFAULT"] = {
                    "username": self.usernameLineEdit.text(),
                    "password": self.passwordLineEdit.text(),
                    "remember_username": self.checkBox.isChecked(),
                    "remember_password": self.checkBox_2.isChecked()
                }
            # 记住账号
            elif self.checkBox.isChecked():
                config["DEFAULT"] = {
                    "username": self.usernameLineEdit.text(),
                    "password": "",
                    "remember_username": self.checkBox.isChecked(),
                    "remember_password": self.checkBox_2.isChecked()
                }
            else:
                config["DEFAULT"] = {
                    "username": "",
                    "password": "",
                    "remember_username": self.checkBox.isChecked(),
                    "remember_password": self.checkBox_2.isChecked()
                }
            with open('user.cfg', 'w')as configfile:
                config.write(configfile)
            # 建立连接，开启消息发送线程
            connect_server.connect()
            MessageSender().start()
            MessageReceiver().start()
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

    # 加载配置文件
    def load_config(self):
        config = configparser.ConfigParser()
        file = config.read('user.cfg')
        config_dict = config.defaults()

        try:
            username = config_dict['username']
            if config_dict['remember_username'] == 'True':
                self.usernameLineEdit.setText(username)
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
            if config_dict['remember_password'] == 'True':
                password = config_dict['password']
                self.passwordLineEdit.setText(password)
                self.checkBox.setChecked(True)
                self.checkBox_2.setChecked(True)
            else:
                self.checkBox_2.setChecked(False)
        except KeyError:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)

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

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()


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
