import base64
import datetime
import sys
import json
import queue
from urllib.parse import urlparse

import requests
from PyQt5.QtCore import QDate, QThread, pyqtSignal, Qt, QSize, QTimer, QFileInfo
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor, QKeySequence, QIcon
from qtpy import QtCore
from chatWindow.chatWindow import Ui_Form
from chatWindow.chatWindowNew import Ui_Form as u
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QTextBrowser, QFileDialog
from globalFile import GlobalData
from utils import record_voice
from utils.notice_sender import NotificationWindow
from utils.md5_ import getFileMd5
from voice_call.callVoiceCallWindow import VoicePhoneWindow

from richTextEditorWindow.richText import RichTextWindow

global_data = GlobalData()


class MessageReceiver(QThread):
    receive_signal = pyqtSignal(object)

    def run(self):
        while True:
            try:
                newMessage = global_data.message_receive_queue.get(timeout=0.2)
                self.receive_signal.emit(newMessage)
            except queue.Empty:
                pass


class ChatWindow(QMainWindow, u):
    def __init__(self, chatList=[], token=""):
        super(ChatWindow, self).__init__()
        self.setupUi(self)
        # 聊天码
        self.chatNumber = chatList[0]
        global_data.chat_user = self.chatNumber
        self.chatUsername = chatList[1]
        # token
        self.token = token
        self.mes_html = '''
                        <body onload="window.scrollTo(0,document.body.scrollHeight); " >
        <style>
        p {
            font-family: 'SimSun';
            font-size: 14px !important;
            font-weight: 400;
            font-style: normal;
        }
        img{
            max-width: 100%;
        }
        * {
            box-sizing: border-box;
        }

        body {
            background-color: #f2f5fa;
        }

        .message {
            display: flex;
            max-width: 50%;
            word-break: break-word;
            margin-top: 30px
        }

        .chat-receiver {
            flex-direction: row-reverse;
            margin-left: auto;
        }

        .chat-sender {
        }

        .avatar {
            max-width: 10%;
            min-width: 10%;
            font-size: 30px;
            border-color: lightyellow;
            background-color: #FFD700;
            /*border-radius: 50%;*/
            height: 55px;
            width: 55px;
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .nickname {
            max-width: 100%;
            flex: 100%;
        }

        .content {
            display: flex;
            flex-wrap: wrap;
            margin-left: 10px;
            margin-right: 10px;
        }

        .text-content {
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
        }

        .sender {
            background-color: #fff;
        }

        .receiver {
            background-color: #b2e281;
        }

        .receiver-name {
            text-align: right;
        }
        .receiver-content{
            justify-content: flex-end;
        }
    </style>'''
        self.mes_sender = '''
        <div class="message chat-sender">
        <div class="avatar">{0}</div>
        <div class="content">
        <div class="nickname">{1} {2}</div>
        <div class="text-content sender">
        '''
        self.mes_receiver = '''
        <div class="message chat-receiver">
        <div class="avatar">{0}</div>
        <div class="content receiver-content">
        <div class="nickname receiver-name">{1} {2}</div>
        <div class="text-content receiver">
        '''
        self.mes_end = '''
        </div>
        </div>
        </div>
        '''
        '''
        样式控制
        '''
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 设置标题
        self.setWindowTitle("聊天 " + self.chatUsername)
        self.setWindowIcon(QtGui.QIcon('imgs/chatroom.png'))
        # 设置日历控件允许弹出
        self.dateTimeEdit_1.setCalendarPopup(True)
        self.dateTimeEdit_1.setDate(QtCore.QDate(2020, 1, 1))
        self.dateTimeEdit_2.setCalendarPopup(True)
        self.dateTimeEdit_2.setDate(QDate.currentDate())
        self.dateTimeEdit_1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_2.setDisplayFormat("yyyy/MM/dd HH-mm-ss")
        # 加载图片
        jpg = QtGui.QPixmap("imgs/file.png").scaled(30, 30)
        self.fileLabel.setPixmap(jpg)
        jpg = QtGui.QPixmap("imgs/phone.png").scaled(30, 30)
        self.phoneLabel.setPixmap(jpg)
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
        # 语音电话
        self.phoneButton.clicked.connect(self.openVoicePhone)
        # 富文本编辑
        self.richTextButton.clicked.connect(self.openRichTextEditor)
        # 电话和语音
        self.fileButton.clicked.connect(self.chooseFile)
        # self.phoneButton.clicked.connect()
        # 启动接收线程
        self.receiver = MessageReceiver()
        self.receiver.receive_signal.connect(self.messageShow)
        self.receiver.start()
        self.messageTextBrowser.page().profile().downloadRequested.connect(self.on_downloadRequested)
        # self.loadMessage()
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
        # 加载表情
        for emojy, emojy_name in zip(self.emojy_list, self.emojy_name_list):
            self.combo.addItem(QIcon(emojy), emojy_name)
        self.combo.currentIndexChanged.connect(self.addEmojy)
        # 加载网页版消息提示框
        # self.messageTextBrowser = QWebEngineView()
        # self.messageTextBrowser.resize(851, 501)
        # self.messageTextBrowser.move(10, 10)

    def show(self) -> None:
        super().show()
        self.loadMessage()

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
                mes_time = message['time']
                mes_content = message['content']
                if mes_username == global_data.self_data['nickname']:
                    mes_username = "我"
                    self.addMessageContent(mes_username, mes_time, mes_content, 1)
                else:
                    self.addMessageContent(mes_username, mes_time, mes_content, 0)

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
            self.sendMessage(currentMessage, 0)

    # 客户端发送消息
    def sendMessage(self, mes, type_):
        content = mes
        # 界面加载消息
        mes_username = "我"
        # 获取UTC+8当前时间
        tzinfo = datetime.timezone(datetime.timedelta(hours=8.0))
        mes_time = datetime.datetime.now(tzinfo).isoformat()
        if type_ == 0:
            # 普通文字消息
            global_data.message_sender_queue.put((self.chatNumber, content))
            self.addMessageContent(mes_username=mes_username, mes_time=mes_time, mes_content=content, type=1)
        # 语音消息
        elif type_ == 1:
            # 语音消息
            mes = "语音消息"
            self.addVoiceMessageContent(mes_username=mes_username, mes_time=mes_time, mes_content=content, type=1)
        # 文件消息
        elif type_ == 2:
            mes = "文件消息"
            self.addFileMessageContent(mes_username, mes_time, content, 1)
        self.clearMessage(1)

    # 客户端显示消息
    def messageShow(self, newMessage):
        if str(newMessage.get('from').get('id')) != str(self.chatNumber) and str(
                newMessage.get('to') != str(self.chatNumber)):
            # 不显示别人的消息
            return
        mes_username = newMessage.get("from").get("nickname")
        mes_content = newMessage.get("content")
        mes_time = newMessage.get('time')
        self.addMessageContent(mes_username=mes_username, mes_time=mes_time, mes_content=mes_content, type=0)

    # 增加语音消息提示
    # todo
    def addVoiceMessageContent(self, mes_username, mes_time, mes_content, type):
        # 他人发送
        if type == 0:
            mes_temp = '''<audio controls="controls" autobuffer="autobuffer">
            <source src="data:audio/wav;base64,''' + mes_content + '''" />语音消息 </audio>'''
            mes_voice = self.mes_sender.format(mes_username[0], mes_username,
                                               datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                                   '%Y-%m-%d %H:%M:%S')) + mes_temp + self.mes_end
            self.mes_html += mes_voice
            self.messageTextBrowser.setHtml(self.mes_html)
        # 自己发送
        else:
            mes_temp = '''<audio controls="controls" autobuffer="autobuffer">
                        <source src="data:audio/wav;base64,''' + mes_content + '''" />语音消息 </audio>'''
            mes_voice = self.mes_receiver.format(mes_username[0], mes_username,
                                                 datetime.datetime.strptime(mes_time,
                                                                            "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                                     '%Y-%m-%d %H:%M:%S')) + mes_temp + self.mes_end
            self.mes_html += mes_voice
            self.messageTextBrowser.setHtml(self.mes_html)
            # 发送消息
        global_data.message_sender_queue.put((self.chatNumber, mes_temp))

    # 增加文件消息提示
    # todo
    def addFileMessageContent(self, mes_username, mes_time, mes_content, type):
        # 他人发送
        if type == 0:
            mes_temp = '''<a href="''' + mes_content + '''" download="file">点击下载文件</a>'''
            mes_file = self.mes_sender.format(mes_username[0], mes_username,
                                              datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                                  '%Y-%m-%d %H:%M:%S'),
                                              mes_content) + mes_temp + self.mes_end
            self.mes_html += mes_file
            self.messageTextBrowser.setHtml(self.mes_html)
        # 自己发送
        else:
            mes_temp = '''<a href="''' + mes_content + '''" download="file">点击下载文件</a>'''
            mes_file = self.mes_receiver.format(mes_username[0], mes_username,
                                                datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                                    '%Y-%m-%d %H:%M:%S'),
                                                mes_content) + mes_temp + self.mes_end
            self.mes_html += mes_file
            self.messageTextBrowser.setHtml(self.mes_html)
        global_data.message_sender_queue.put((self.chatNumber, mes_temp))

    # 增加消息框内容（文本消息）
    def addMessageContent(self, mes_username, mes_time, mes_content, type):
        # HTML加载消息
        # 收到消息
        if type == 0:
            try:  # html自动移至底部
                mes_text = self.mes_sender + '{3}' + self.mes_end
                mes_text = mes_text.format(mes_username[0], mes_username,
                                           datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                               '%Y-%m-%d %H:%M:%S'),
                                           mes_content)
                self.mes_html += mes_text
                self.messageTextBrowser.setHtml(self.mes_html)
            except ValueError:
                mes_text = self.mes_sender + '{3}' + self.mes_end
                mes_text = mes_text.format(mes_username[0], mes_username,
                                           datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S%z").strftime(
                                               '%Y-%m-%d %H:%M:%S'),
                                           mes_content)
                self.mes_html += mes_text
                self.messageTextBrowser.setHtml(self.mes_html)
        # 自己发送
        else:
            try:  # html自动移至底部
                mes_text = self.mes_receiver + '{3}' + self.mes_end
                mes_text = mes_text.format(mes_username[0], mes_username,
                                           datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                                               '%Y-%m-%d %H:%M:%S'),
                                           mes_content)
                self.mes_html += mes_text
                self.messageTextBrowser.setHtml(self.mes_html)
            except ValueError:
                mes_text = self.mes_receiver + '{3}' + self.mes_end
                mes_text = mes_text.format(mes_username[0], mes_username,
                                           datetime.datetime.strptime(mes_time, "%Y-%m-%dT%H:%M:%S%z").strftime(
                                               '%Y-%m-%d %H:%M:%S'),
                                           mes_content)
                self.mes_html += mes_text
                self.messageTextBrowser.setHtml(self.mes_html)

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
            # 可能出现timeoutError
            try:
                record = global_data.record_queue.get()
                self.sendMessage(record, type_=1)
                NotificationWindow.success("提示", "语音成功发送")
            except Exception as e:
                global_data.logger.error(e)
                QMessageBox.warning(self, "警告", "语音消息发送失败！", QMessageBox.Yes)

    # 选择并发送文件
    def chooseFile(self):
        try:
            file_, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/", "All Files (*);;Text Files (*.txt)")
            # print(file_)
            # print(filetype)
            query_url = global_data.base_url + "/file/query"
            file_md5 = getFileMd5(file_)
            query_data = {"file_md5": str(file_md5)}
            headers = {"Authorization": self.token}
            r = requests.get(url=query_url, headers=headers, params=query_data, proxies=global_data.proxies)
            mes = r.json().get("mes")
            # print(r.text)
            # 需要上传
            if mes:
                headers = {"Authorization": self.token}
                load_url = global_data.base_url + "/file/"
                files = {
                    'file': (file_, open(file_, 'rb'))
                }
                r_load = requests.post(url=load_url, headers=headers, files=files, proxies=global_data.proxies)
                mes = r_load.json().get("mes")
                file_path = r_load.json().get("data")
            # 直接返回链接
            else:
                file_path = r.json().get("data")
            file_text = global_data.base_url + "/" + file_path
            print(file_text)
            self.sendMessage(mes=file_text, type_=2)
        except:
            pass

    # 下载信号连接到的槽
    def on_downloadRequested(self, download: "QWebEngineDownloadItem"):
        # download是QWebEngineDownloadItem对象；
        download.downloadProgress.connect(self._downloadProgress)
        download.finished.connect(self._finished)
        # 下载文件的保存路径及文件名
        old_path = download.path()
        suffix = QFileInfo(old_path).suffix()
        # 下载文件类型
        filttype = download.mimeType()
        # 后缀切割
        unkonw_suffix = filttype.split(r'/')[-1]
        path, _ = QFileDialog.getSaveFileName(self, "Save File", old_path,
                                              "*." + unkonw_suffix + ";;" + "*." + suffix)
        # print(old_path, suffix)
        if path != "":
            download.setPath(path)
            download.accept()

    def _downloadProgress(self, bytesReceived: "qint64", bytesTotal: "qint64"):
        # bytesReceived 当前下载值 ； bytesTotal 文件总大小值
        # self.bytesReceived = bytesReceived
        # self.bytesTotal = bytesTotal
        pass
        # print(bytesReceived, bytesTotal)

    def _finished(self):
        print("下载完成")

    # 语音电话
    def openVoicePhone(self):
        self.voicePhone = VoicePhoneWindow({})
        self.voicePhone.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ChatWindow()

    with open('css/chatWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
