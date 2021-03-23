"""
登录界面
"""

import sys
import requests
import json

from client.forgetPasswordWindow.forgetPasswordWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit


class UserRegisterWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super(UserRegisterWindow, self).__init__()
        self.setupUi(self)
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 重置密码事件
        self.resetButton.clicked.connect(self.userResetPassword)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit_2.setEchoMode(QLineEdit.Password)
        # 发送验证码
        self.sendCodeButton.clicked.connect(self.sendCode)

    # 注册事件
    def userResetPassword(self):
        pwd1 = self.passwordLineEdit.text()
        pwd2 = self.passwordLineEdit_2.text()
        email = self.emailLineEdit.text()
        code = self.codeLineEdit.text()
        if pwd1 == "" or pwd2 == "":
            QMessageBox.warning(self, "警告", "请输入密码！", QMessageBox.Yes)
        elif pwd1 != pwd2:
            QMessageBox.warning(self, "警告", "两次密码不一致！", QMessageBox.Yes)
        elif email == "":
            QMessageBox.warning(self, "警告", "请输入邮箱！", QMessageBox.Yes)
        elif code == "":
            QMessageBox.warning(self, "警告", "请填写验证码！", QMessageBox.Yes)
        # 重置密码
        else:
            resetData = {"email": email, "password": pwd1, "code": code}
            url = "http://sqq.12138.site:1234/users/password"
            r = requests.put(url, data=resetData)
            mes = json.loads(r.text)['mes']
            # 重置成功
            if mes == "":
                QMessageBox.information(self, "提示", "密码重置成功！", QMessageBox.Yes)
                self.close()
            # 提示问题
            else:
                QMessageBox.warning(self, "警告", "{0}".format(json.loads(r.text)['mes']), QMessageBox.Yes)

    # 发送验证码
    def sendCode(self):
        url = ""
        mes = 1
        if mes == 1:
            QMessageBox.warning(self, "警告", "两次发送验证码时间\n间隔不能小于一分钟！", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "发送成功！请注意查收！", QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = UserRegisterWindow()

    with open('../css/forgetWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
