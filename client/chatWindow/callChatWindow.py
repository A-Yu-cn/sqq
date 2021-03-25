import datetime
import sys
import requests
from PyQt5.QtCore import QDate
from qtpy import QtCore
from client.golbalFile import base_url
from client.localClient import localClient

from client.chatWindow.chatWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class ChatWindow(QMainWindow, Ui_Form):

    def __init__(self, chatList=[], token=""):
        super(ChatWindow, self).__init__()
        self.setupUi(self)
        # 聊天码
        self.chatNumber = chatList[0]
        self.chatUsername = chatList[1]
        # token
        self.token = token
        '''
        样式控制
        '''
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 设置标题
        self.setWindowTitle("聊天 " + self.chatUsername)
        # 设置日历控件允许弹出
        self.dateTimeEdit_1.setCalendarPopup(True)
        self.dateTimeEdit_1.setDate(QtCore.QDate(2020, 1, 1))
        self.dateTimeEdit_2.setCalendarPopup(True)
        self.dateTimeEdit_2.setDate(QDate.currentDate())
        self.dateTimeEdit_1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_2.setDisplayFormat("yyyy/MM/dd HH-mm-ss")
        '''
        逻辑绑定   
        '''
        # 隐藏历史消息
        self.setFixedWidth(870)
        self.widget.hide()
        # 历史记录按钮
        self.historyButton.clicked.connect(self.queryHistoryMessage)
        # 清空按钮
        self.clearButton.clicked.connect(self.clearMessage)
        # 发送按钮
        self.submitButton.clicked.connect(self.submitMessage)
        # 查询按钮
        self.queryHistoryButton.clicked.connect(self.queryHistoryMessageByDate)

    # 发送消息
    def submitMessage(self):
        currentMessage = self.textEdit.toPlainText()
        if currentMessage == "":
            QMessageBox.warning(self, "提示", "请输入内容！", QMessageBox.Yes)

    # 查询历史消息
    def queryHistoryMessage(self):
        if self.width() == 870:
            self.setFixedWidth(1119)
            self.widget.show()
            self.loadHistoryMessage()
        else:
            self.setFixedWidth(870)
            self.widget.hide()

    # 加载历史消息
    def loadHistoryMessage(self):
        mes_username = ""
        mes_time = ""
        mes_content = ""
        for i in range(0, 100):
            mes_username = "hx"
            mes_time = "2021-03-17 10:02:20"
            mes_content = "666"
            self.historyTextBrowser.append('<h3 style="color:blue;">{0}\t{1}</h3>'.format(mes_username, mes_time))
            self.historyTextBrowser.append(
                '<p style="background-color:lightyellow;color:black;">{0}</p>\n'.format(
                    mes_content))
            # self.historyTextBrowser.append('<img src="logo.png"/>')

    # 清空输入框
    def clearMessage(self):
        choice = QMessageBox.information(self, "提示", "清空输入框内容？", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.textEdit.setText("")

    # 接收消息事件
    def receiveMessage(self):
        pass

    # 根据时间查询历史记录
    def queryHistoryMessageByDate(self):
        dt1 = self.dateTimeEdit_1.dateTime().toPyDateTime().replace(tzinfo=datetime.timezone.utc).isoformat()
        dt2 = self.dateTimeEdit_2.dateTime().toPyDateTime().replace(tzinfo=datetime.timezone.utc).isoformat()
        # 获取历史消息
        self.getHisMessage(dt1, dt2)
        print(dt1)
        print(dt2)

    # 查询历史消息请求
    def getHisMessage(self, dt1, dt2):
        url = base_url + "/message"
        headers = {"Authorization": self.token}
        data = {"other_id": self.chatNumber, "start_time": dt1, "end_time": dt2}
        r = requests.get(url=url, json=data, headers=headers)
        print(r)
        print(r.text)

    # 发送消息
    def sendMessage(self, mes):
        cl = localClient.Client()
        cl.client.sendall(cl.wrap_message(mes))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ChatWindow()

    with open('../css/chatWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
