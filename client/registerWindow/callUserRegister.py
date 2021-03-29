"""
登录界面
"""

import sys
import requests
import json

from registerWindow.userRegister import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from golbalFile import base_url
from PyQt5.QtGui import QIcon


class UserRegisterWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super(UserRegisterWindow, self).__init__()
        self.setWindowIcon(QIcon('../imgs/register.png'))
        self.setupUi(self)
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 注册事件
        self.registerButton.clicked.connect(self.userRegister)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit_2.setEchoMode(QLineEdit.Password)
        # 发送验证码
        self.sendCodeButton.clicked.connect(self.sendCode)

    # 注册事件
    def userRegister(self):
        username = self.usernameLineEdit.text()
        pwd1 = self.passwordLineEdit.text()
        pwd2 = self.passwordLineEdit_2.text()
        email = self.emailLineEdit.text()
        code = self.codeLineEdit.text()
        if username == "":
            QMessageBox.warning(self, "警告", "请输入用户名！", QMessageBox.Yes)
        elif pwd1 == "" or pwd2 == "":
            QMessageBox.warning(self, "警告", "请输入密码！", QMessageBox.Yes)
        elif pwd1 != pwd2:
            QMessageBox.warning(self, "警告", "两次密码不一致！", QMessageBox.Yes)
        elif email == "":
            QMessageBox.warning(self, "警告", "请输入邮箱！", QMessageBox.Yes)
        elif code == "":
            QMessageBox.warning(self, "警告", "请填写验证码！", QMessageBox.Yes)
        # 注册
        else:
            regData = {"email": email, "nickname": username, "password": pwd1}
            url = base_url + "/users/"
            r = requests.post(url, json=regData)
            mes = json.loads(r.text)['mes']
            # 注册成功
            if mes == "":
                QMessageBox.information(self, "提示", "恭喜你，注册成功！\n请牢记您的登录账号:{0}".format(json.loads(r.text)['data']),
                                        QMessageBox.Yes)
                self.close()
            # 提示问题
            else:
                QMessageBox.warning(self, "警告", "{0}".format(json.loads(r.text)['mes']), QMessageBox.Yes)

    # 发送验证码
    def sendCode(self):
        email = self.emailLineEdit.text()
        if '@' not in email:
            QMessageBox.warning(self, '警告', '邮箱输入有误')
            return
        url = base_url + "/code"
        data = {"email": self.emailLineEdit.text(), "type": "1"}
        r = requests.get(url=url, params=data)
        print(r.text)
        print(r.json())
        if r.json().get("mes"):
            QMessageBox.warning(self, "警告", "{0}".format(r.json().get("mes")), QMessageBox.Yes)
            return
        else:
            QMessageBox.information(self, "提示", "发送成功！请注意查收！", QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = UserRegisterWindow()

    with open('../css/userRegister.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
