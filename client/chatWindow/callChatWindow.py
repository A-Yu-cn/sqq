import _queue
import base64
import datetime
import sys
import time

import requests
from PyQt5.QtCore import QDate, QThread, pyqtSignal, Qt, QSize, QTimer, QDateTime, QUrl
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor, QKeySequence, QIcon
from qtpy import QtCore
import localClient
from threading import Thread
from chatWindow.chatWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox
from globalFile import GlobalData
from utils import record_voice
from utils.notice_sender import NotificationWindow

global_data = GlobalData()
from richTextEditorWindow.richText import RichTextWindow


class MessageReceiver(QThread):
    receive_signal = pyqtSignal(object)

    def run(self):
        while True:
            newMessage = global_data.message_receive_queue.get()
            self.receive_signal.emit(newMessage)


class ChatWindow(QMainWindow, Ui_Form):

    def __init__(self, chatList=[], token=""):
        super(ChatWindow, self).__init__()
        self.setupUi(self)
        # 聊天码
        self.chatNumber = chatList[0]
        global_data.chat_user = self.chatNumber
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
        self.setWindowIcon(QtGui.QIcon('../imgs/chatroom.png'))
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
        seq = QKeySequence(Qt.CTRL + Qt.Key_Return)
        self.submitButton.setShortcut(seq)
        # 查询按钮
        self.queryHistoryButton.clicked.connect(self.queryHistoryMessageByDate)
        # 录制语音按钮
        self.recordButton.clicked.connect(self.record)
        # 初始化一个定时器
        self.timer = QTimer(self)
        # 将定时器超时信号与槽函数连接
        self.timer.timeout.connect(self.showTime)
        self.time_text = 0
        # 设置语音发送模块初始样式
        self.recordLabel.hide()
        self.cancleButton.hide()
        # 取消发送
        self.cancleButton.clicked.connect(self.cancleRecord)
        # 富文本编辑
        self.richTextButton.clicked.connect(self.openRichTextEditor)
        # 启动接收线程
        self.receiver = MessageReceiver()
        self.receiver.receive_signal.connect(self.messageShow)
        self.receiver.start()
        self.loadMessage()
        # 添加表情
        self.combo = QComboBox(self)
        self.combo.resize(100, 40)
        size = QSize(35, 35)
        self.combo.setIconSize(size)
        self.combo.move(620, 520)
        self.emojy_list = ["emojy/001-anxious.png", "emojy/002-crying.png", "emojy/003-dizzy.png",
                           "emojy/005-blowkiss.png", "emojy/006-full.png",
                           "emojy/008-vomiting.png",
                           "emojy/009-laughing.png", "emojy/010-rollingeyes.png",
                           "emojy/012-laughing.png", "emojy/013-flushed.png",
                           "emojy/015-grinning.png",
                           "emojy/017-hug.png", "emojy/018-crying.png", "emojy/019-angry.png",
                           "emojy/020-sleeping.png", "emojy/021-fallinlove.png",
                           "emojy/022-smilingface.png", "emojy/025-thinking.png",
                           "emojy/026-tired.png",
                           "emojy/027-unamused.png"]
        self.emojy_name_list = ['焦虑', '哭', '懒', '飞吻', '满足', '呕吐', '大笑', '白眼', '笑哭', '害羞', '汗', '拥抱', '泪', '生气', '睡觉',
                                '喜欢', '微笑', '思考', '困倦', '斜眼']
        for emojy, emojy_name in zip(self.emojy_list, self.emojy_name_list):
            self.combo.addItem(QIcon(emojy), emojy_name)
        self.combo.currentIndexChanged.connect(self.addEmojy)

    def loadMessage(self):
        # 获取当天零点和24点
        tzinfo = datetime.timezone(datetime.timedelta(hours=8.0))
        now = datetime.datetime.now(tzinfo)
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                             microseconds=now.microsecond)
        lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)

        # 获取当天内的消息
        message = self.getHisMessage(zeroToday.isoformat(), lastToday.isoformat())
        if message.get('mes'):
            QMessageBox.warning('警告', message.get('mes'))
        else:
            for message in message.get('data').get('message_list'):
                mes_username = message['from']['nickname']
                mes_username = "我" if mes_username == global_data.self_data['nickname'] else mes_username
                mes_time = message['time']
                mes_content = message['content']
                self.addMessageContent(mes_username, mes_time, mes_content)

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
                        .format(mes_username, mes_userid,
                                datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                    '%Y-%m-%d %H:%M:%S')))
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
        currentMessageText = self.textEdit.toPlainText()
        currentMessage = self.textEdit.toHtml()
        if currentMessageText == "":
            QMessageBox.warning(self, "提示", "请输入内容！", QMessageBox.Yes)
        else:
            self.sendMessage(currentMessage)

    # 客户端发送消息
    def sendMessage(self, mes):
        global_data.message_sender_queue.put((self.chatNumber, mes))
        # 界面加载消息
        mes_username = "我"
        mes_content = mes
        # 获取UTC+8当前时间
        tzinfo = datetime.timezone(datetime.timedelta(hours=8.0))
        mes_time = datetime.datetime.now(tzinfo).isoformat()
        self.addMessageContent(mes_username=mes_username, mes_time=mes_time, mes_content=mes_content)
        self.clearMessage(1)

    # 客户端显示消息
    def messageShow(self, newMessage):
        mes_username = newMessage.get("from").get("nickname")
        mes_content = newMessage.get("content")
        mes_time = newMessage.get('time')
        self.addMessageContent(mes_username=mes_username, mes_time=mes_time, mes_content=mes_content)

    # 打开富文本编辑器
    def openRichTextEditor(self):
        self.richText = RichTextWindow()
        self.richText.Signal.connect(self.updateRichTextMessage)
        self.richText.show()

    # 更新富文本消息
    def updateRichTextMessage(self, mes_html):
        self.textEdit.setText(mes_html)

    def __del__(self):
        self.receiver.terminate()

    # 这里是关闭聊天窗口
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        global_data.chat_user = 0
        # 关闭消息接收线程
        self.receiver.terminate()

    # 增加消息框内容
    def addMessageContent(self, mes_username, mes_time, mes_content):
        try:
            self.messageTextBrowser.append(
                '<p style="color:blue;">{0}\t\t<text style="color:lightblue;">{1}</text></p>'
                    .format(mes_username,
                            datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                '%Y-%m-%d %H:%M:%S')))
        except ValueError:
            self.messageTextBrowser.append(
                '<p style="color:blue;">{0}\t\t<text style="color:lightblue;">{1}</text></p>'
                    .format(mes_username,
                            datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S%z").strftime(
                                '%Y-%m-%d %H:%M:%S')))
        self.messageTextBrowser.append('{0}\n'.format(mes_content))
        # 添加消息后将光标滚到最底下
        self.messageTextBrowser.moveCursor(QTextCursor.End)

    # 添加表情
    def addEmojy(self):
        emojy_index = self.combo.currentIndex()
        emojy = self.emojy_list[emojy_index]
        with open(emojy, "rb") as f:  # 转为二进制格式
            base64_data = base64.b64encode(f.read()).decode()  # 使用base64进行加密
            img_data = '<img src="data:image/bmp;base64,' + base64_data + '">'
            self.textEdit.append(img_data)

    # 改变时间显示
    def showTime(self):
        # 在标签上显示时间
        self.time_text += 1
        time_text_show = ""
        if self.time_text > 30:
            self.endRecord()
        elif self.time_text < 10:
            time_text_show = "00:0" + str(self.time_text)
        else:
            time_text_show = "00:" + str(self.time_text)
        self.recordLabel.setText(time_text_show)

    # 停止录制
    def endRecord(self):
        self.timer.stop()
        global_data.record_signal = False
        self.time_text = 0
        self.recordLabel.setText("00:00")
        self.recordLabel.hide()
        self.cancleButton.hide()
        self.recordButton.setText("发送语音")

    # 取消录制
    def cancleRecord(self):
        self.endRecord()
        NotificationWindow.info('提示', '停止录制语音')

    # 录制语音
    def record(self):
        # 开始录音
        if self.recordButton.text() == "发送语音":
            global_data.record_signal = True
            self.timer.start(1000)  # 设置计时间隔并启动，每隔1000毫秒（1秒）发送一次超时信号，循环进行
            record_voice.Recorder().start()
            self.recordLabel.show()
            self.cancleButton.show()
            self.recordButton.setText("停止并发送")
            NotificationWindow.success('提示', '开始录制语音')
        elif self.recordButton.text() == "停止并发送":
            self.endRecord()
            NotificationWindow.success("提示", "语音成功发送")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ChatWindow()

    with open('../css/chatWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
