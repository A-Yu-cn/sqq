import sys

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QDate
from qtpy import QtCore

from .chatWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class ChatWindow(QMainWindow, Ui_Form):

    def __init__(self):
        super(ChatWindow, self).__init__()
        self.setupUi(self)
        '''
        样式控制
        '''
        # 禁止拉伸窗口
        self.setFixedSize(self.width(), self.height())
        # 设置日历控件允许弹出
        self.dateTimeEdit_1.setCalendarPopup(True)
        self.dateTimeEdit_1.setDate(QtCore.QDate(2020, 1, 1))
        self.dateTimeEdit_2.setCalendarPopup(True)
        self.dateTimeEdit_2.setDate(QDate.currentDate())
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
        self.historyTextBrowser.setText()
        pass

    # 清空输入框
    def clearMessage(self):
        choice = QMessageBox.information(self, "提示", "清空输入框内容？", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.textEdit.setText("")

    # 接收消息事件
    def receiveMessage(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ChatWindow()

    myWin.show()

    sys.exit(app.exec_())
