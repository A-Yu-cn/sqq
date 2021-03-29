import sys
import requests
from PyQt5.QtCore import pyqtSignal
import json

from startGroup.startGroup import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from golbalFile import base_url


class GroupWindow(QMainWindow, Ui_Form):
    # 信号
    my_Signal = pyqtSignal(str)

    def __init__(self, friendList=[], token=""):
        super(GroupWindow, self).__init__()
        self.setupUi(self)
        self.friendList = friendList
        self.token = token
        # 绑定按钮
        self.startGroupButton.clicked.connect(self.startGroup)
        self.chooseAllButton.clicked.connect(self.chooseAll)
        self.cancleChooseAllButton.clicked.connect(self.cancelChooseAll)
        # 加载好友
        for i in self.friendList:
            _item = QtWidgets.QListWidgetItem(i[1])
            _item.setCheckState(0)
            self.listWidget.addItem(_item)

    # 全选
    def chooseAll(self):
        count = self.listWidget.count()  # 得到QListWidget的总个数
        for i in range(count):
            self.listWidget.itemWidget(self.listWidget.item(i).setCheckState(Qt.Checked))

    # 取消全选
    def cancelChooseAll(self):
        count = self.listWidget.count()  # 得到QListWidget的总个数
        for i in range(count):
            self.listWidget.itemWidget(self.listWidget.item(i).setCheckState(Qt.Unchecked))

    # 发起群聊
    def startGroup(self):
        groupName = self.lineEdit.text()
        if groupName == "":
            QMessageBox.warning(self, "警告", "给聊天室起个名字吧！", QMessageBox.Yes)
            return
        count = self.listWidget.count()  # 得到QListWidget的总个数
        chooses = []  # 存放被选择的数据
        state = 0
        for i in range(count):
            if self.listWidget.item(i).checkState() == 2:
                state = 1
                chooses.append(self.friendList[i][0])
        if not state:
            QMessageBox.warning(self, "警告", "你至少要选择一个好友！", QMessageBox.Yes)
            return
        else:
            url = base_url + "/chatroom/"
            headers = {"Authorization": self.token}
            startData = {"friend_ids": chooses, "name": groupName}
            r = requests.post(url=url, json=startData, headers=headers)
            try:
                if json.loads(r.text)["mes"]:
                    QMessageBox.warning(self, "警告", "添加失败！\n原因:{0}".format(json.loads(r.text)["mes"]), QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "群聊添加成功！", QMessageBox.Yes)
                    self.sendEditContent()
                    self.destroy()
                return
            except KeyError:
                QMessageBox.warning(self, "警告", "添加失败！", QMessageBox.Yes)

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = GroupWindow()

    with open('../css/startGroup.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
