import sys
import requests
from PyQt5.QtCore import pyqtSignal

from listWindow.addUserAndGroup import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from globalFile import GlobalData
from startGroup.callStartGroup import GroupWindow
from PyQt5 import QtGui

global_data = GlobalData()

TextStyle = """
    QMessageBox QPushButton[text="OK"] {
        qproperty-text: "添加好友";
    }
    QMessageBox QPushButton[text="Open"] {
        qproperty-text: "打开";
    }
    QMessageBox QPushButton[text="Save"] {
        qproperty-text: "保存";
    }
    QMessageBox QPushButton[text="Cancel"] {
        qproperty-text: "取消";
    }
    QMessageBox QPushButton[text="Close"] {
        qproperty-text: "关闭";
    }
    QMessageBox QPushButton[text="Discard"] {
        qproperty-text: "不保存";
    }
    QMessageBox QPushButton[text="Don't Save"] {
        qproperty-text: "不保存";
    }
    QMessageBox QPushButton[text="Apply"] {
        qproperty-text: "加入群聊";
    }
    QMessageBox QPushButton[text="Reset"] {
        qproperty-text: "重置";
    }
    QMessageBox QPushButton[text="Restore Defaults"] {
        qproperty-text: "恢复默认";
    }
    QMessageBox QPushButton[text="Help"] {
        qproperty-text: "帮助";
    }
    QMessageBox QPushButton[text="Save All"] {
        qproperty-text: "保存全部";
    }
    QMessageBox QPushButton[text="&Yes"] {
        qproperty-text: "好的";
    }
    QMessageBox QPushButton[text="Yes to &All"] {
        qproperty-text: "全部都是";
    }
    QMessageBox QPushButton[text="&No"] {
        qproperty-text: "不";
    }
    QMessageBox QPushButton[text="N&o to All"] {
        qproperty-text: "全部都不";
    }
    QMessageBox QPushButton[text="Abort"] {
        qproperty-text: "终止";
    }
    QMessageBox QPushButton[text="Retry"] {
        qproperty-text: "加入群聊";
    }
    QMessageBox QPushButton[text="Ignore"] {
        qproperty-text: "忽略";
    }
    QPushButton#searchButton,#startGroupButton{
    color: #fff;
    border:1px solid transparent;
    background-color: #007bff;
    border-radius: 3px;
    }
    QLineEdit{
    border: 1px solid #ccc;
    border-radius: 4px;
    }
    QLineEdit:focus{
    outline: 0;
    border: 2px solid #80bdff;
    }
    """


class AddWindow(QMainWindow, Ui_Form):
    # 信号
    my_Signal = pyqtSignal(str)

    def __init__(self, loginInfo={}, token=""):
        super(AddWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("添加")
        self.setWindowIcon(QtGui.QIcon('imgs/chatroom.png'))
        self.loginInfo = loginInfo
        self.token = token
        self.setStyleSheet(TextStyle)
        # 绑定按钮
        self.startGroupButton.clicked.connect(self.startGroup)
        self.searchButton.clicked.connect(self.searchInfo)

    # 搜索
    def searchInfo(self):
        try:
            search_id = self.idLineEdit.text()
            if search_id == "":
                QMessageBox.warning(self, "提示", "请输入ID！", QMessageBox.Yes)
                return
            else:
                url = global_data.base_url + "/query/" + search_id
                r = requests.get(url=url)
                user_data = r.json()
                if user_data.get("mes"):
                    QMessageBox.warning(self, "提示", "出现错误！\n原因:{0}".format(user_data.get("mes")), QMessageBox.Yes)
                    return
                else:
                    user_id = user_data.get("data").get("id")
                    user_name = user_data.get("data").get("name")
                    if len(str(user_id)) == 5:
                        user_email = user_data.get("data").get("email")
                        reply = QMessageBox.information(self, "用户信息",
                                                        "用户ID: {0}\n用户姓名: {1}\n 用户邮箱: {2}".format(user_id, user_name,
                                                                                                  user_email),
                                                        QMessageBox.Ok | QMessageBox.Cancel)
                        if reply == QMessageBox.Ok:
                            self.addFriend(user_id)
                        else:
                            return
                    else:
                        reply = QMessageBox.information(self, "群聊信息",
                                                        "群聊ID: {0}\n 群聊名称: {1}".format(user_id, user_name),
                                                        QMessageBox.Retry | QMessageBox.Cancel)
                        if reply == QMessageBox.Retry:
                            self.joinGroup(user_id)
                        else:
                            return
        except KeyError:
            pass

    # 添加好友
    def addFriend(self, f_id):
        f_id = f_id
        if f_id == "":
            QMessageBox.warning(self, "提示", "请输入好友码！", QMessageBox.Yes)
        else:
            url = global_data.base_url + "/users/friends"
            addData = {"friend_id": int(f_id)}
            try:
                headers = {"Authorization": self.token}
                r = requests.post(url, json=addData, headers=headers, proxies=global_data.proxies)
            except KeyError:
                QMessageBox.warning(self, "警告", "您的用户Token无效！", QMessageBox.Yes)
                return
            mes = r.json().get("mes")
            if mes:
                QMessageBox.warning(self, "警告", "添加失败！\n原因: {0}".format(mes), QMessageBox.Yes)
            # 添加成功
            else:
                QMessageBox.information(self, "提示", "添加成功！", QMessageBox.Yes)

    # 加入群聊
    def joinGroup(self, f_id):
        f_id = f_id
        if f_id == "":
            QMessageBox.warning(self, "提示", "请输入好友码！", QMessageBox.Yes)
        else:
            url = global_data.base_url + "/chatroom/"
            addData = {"chatroom_id": int(f_id)}
            print(addData)
            try:
                headers = {"Authorization": self.token}
                r = requests.put(url, json=addData, headers=headers, proxies=global_data.proxies)
            except KeyError:
                QMessageBox.warning(self, "警告", "您的用户Token无效！", QMessageBox.Yes)
                return
            mes = r.json().get("mes")
            if mes:
                QMessageBox.warning(self, "警告", "添加失败！\n原因: {0}".format(mes), QMessageBox.Yes)
            # 添加成功
            else:
                QMessageBox.information(self, "提示", "添加成功！", QMessageBox.Yes)

    # 发起群聊
    def startGroup(self):
        try:
            self.groupWindow = GroupWindow(self.loginInfo['data']['friends'], self.token)
            with open('css/startGroup.css') as file:
                qss = file.readlines()
                qss = ''.join(qss).strip('\n')
            self.groupWindow.setStyleSheet(qss)
            self.groupWindow.show()
        except KeyError:
            QMessageBox.warning(self, "警告", "用户认证无效！", QMessageBox.Yes)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = AddWindow()

    myWin.show()

    sys.exit(app.exec_())
