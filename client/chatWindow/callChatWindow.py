import datetime
import sys
import requests
from PyQt5.QtCore import QDate
from qtpy import QtCore
import localClient
from threading import Thread
from chatWindow.chatWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from golbalFile import GlobalData

global_data = GlobalData()
from richTextEditorWindow.richText import RichTextWindow


class ChatWindow(QMainWindow, Ui_Form):

    def __init__(self, chatList=[], token=""):
        super(ChatWindow, self).__init__()
        self.setupUi(self)
        # 聊天码
        self.chatNumber = chatList[0]
        self.chatUsername = chatList[1]
        # token
        self.token = token
        # 建立客户端连接
        self.cl = localClient.Client(self.token, self.chatNumber)
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
        # 富文本编辑
        self.richTextButton.clicked.connect(self.openRichTextEditor)
        # 接收消息
        self.cl.t = Thread(target=self.cl.recv, args=(self.cl.client,))
        self.cl.t.start()

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
    def loadHistoryMessage(self, data={}):
        self.historyTextBrowser.clear()
        mes_username = ""
        mes_time = ""
        mes_content = ""
        # print(data)
        try:
            for i in data['data']['message_list']:
                mes_username = i.get("from").get("nickname")
                mes_userid = i.get("from").get("id")
                mes_time = i.get("time")
                mes_content = i.get("content")
                self.historyTextBrowser.append(
                    '<h3 style="color:blue;">{0}({1})\n<h4 style="color:lightblue;">{2}</h4></h3>'
                        .format(mes_username, mes_userid, str(datetime.datetime.now().fromisoformat(mes_time))))
                self.historyTextBrowser.append('{0}\n'.format(mes_content))
                # self.historyTextBrowser.append('<img src="logo.png"/>')
        except KeyError:
            return

    # 根据时间查询历史记录
    def queryHistoryMessageByDate(self):
        dt1 = self.dateTimeEdit_1.dateTime().toPyDateTime().replace(tzinfo=datetime.timezone.utc).isoformat()
        dt2 = self.dateTimeEdit_2.dateTime().toPyDateTime().replace(tzinfo=datetime.timezone.utc).isoformat()
        # 获取历史消息
        data = self.getHisMessage(dt1, dt2)
        self.loadHistoryMessage(data)
        # print(dt1)
        # print(dt2)

    # 查询历史消息请求
    def getHisMessage(self, dt1, dt2):
        url = global_data.base_url + "/message"
        headers = {"Authorization": self.token}
        data = {"other_id": self.chatNumber, "start_time": dt1, "end_time": dt2}
        r = requests.get(url=url, json=data, headers=headers, proxies=global_data.proxies)
        # print(r)
        # print(r.text)
        try:
            return r.json()
        except ValueError:
            QMessageBox.warning(self, "警告", "查询失败，请重试！", QMessageBox.Yes)
            return

    # 清空输入框
    def clearMessage(self, flag=0):
        if flag == 0:
            choice = QMessageBox.information(self, "提示", "清空输入框内容？", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.textEdit.setText("")
        else:
            self.textEdit.setText("")

    # 发送消息
    def submitMessage(self):
        currentMessage = self.textEdit.toHtml()
        if currentMessage == "":
            QMessageBox.warning(self, "提示", "请输入内容！", QMessageBox.Yes)
        else:
            self.sendMessage(currentMessage)

    # 客户端发送消息
    def sendMessage(self, mes):
        # socket发送消息
        self.cl = localClient.Client(self.token, self.chatNumber)
        self.cl.sendMessage(mes)
        # 界面加载消息
        mes_username = "我"
        mes_time = str(datetime.datetime.now().isoformat())
        mes_content = mes
        self.messageTextBrowser.append(
            '<p style="color:blue;">{0}\t\t<text style="color:lightblue;">{1}</text></p>'
                .format(mes_username, str(datetime.datetime.now().fromisoformat(mes_time))))
        self.messageTextBrowser.append('{0}\n'.format(mes_content))
        self.clearMessage(1)

    # 发送消息并创建用户消息目录

    # 接收消息事件
    def receiveMessage(self):
        self.cl.recv()

    # 打开富文本编辑器
    def openRichTextEditor(self):
        self.richText = RichTextWindow()
        self.richText.Signal.connect(self.updateRichTextMessage)
        self.richText.show()

    # 更新富文本消息
    def updateRichTextMessage(self, mes_html):
        self.textEdit.setText(mes_html)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ChatWindow()

    with open('../css/chatWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
