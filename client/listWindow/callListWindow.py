from datetime import datetime
import json
import sys
import time
import os

import requests
from PyQt5.QtGui import QCursor, QFont

from listWindow.userListWindow import Ui_Form
from chatWindow.callChatWindow import ChatWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QWidget, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy, QTreeWidget, QMessageBox, QMenu, QAction, QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from globalFile import GlobalData

global_data = GlobalData()
from startGroup.callStartGroup import GroupWindow


# 内嵌自定义item对象
class ItemWidget(QWidget):
    def __init__(self, text):
        super(ItemWidget, self).__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # label1 = QLabel(text[0], self, styleSheet='color:yellow;')
        # font = QtGui.QFont()
        # font.setPointSize(40)
        # font.setBold(True)
        # font.setWeight(75)
        # label1.setFont(font)
        label2 = QLabel(text, self, styleSheet='color: black;font-size:20px;')
        # layout.addWidget(label1)
        layout.addWidget(label2)
        # layout.addSpacerItem(QSpacerItem(
        #     60, 1, QSizePolicy.Maximum, QSizePolicy.Minimum))


class ListWindow(QMainWindow, Ui_Form):

    def __init__(self, loginInfo):
        super(ListWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(loginInfo.get('data').get('self').get('nickname'))
        self.setWindowIcon(QtGui.QIcon('../imgs/user.png'))
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        self.treeWidget.customContextMenuRequested.connect(self.treeWidgetItem_fun)  # 绑定右键点击事件
        # 记录登录信息
        self.treeWidget.header().setVisible(False)
        self.loginInfo = loginInfo
        self.token = global_data.token
        # 加载列表
        self.loadList()
        # 隐藏头部
        self.treeWidget.header().setVisible(False)
        # 添加好友按钮
        self.addFriendPushButton.clicked.connect(self.addFriend)
        # 发起群聊按钮
        self.startGroupPushButton.clicked.connect(self.startGroup)
        self.treeWidget.itemDoubleClicked.connect(self.startChat)

    # 加载列表
    def loadList(self):
        count1 = self.treeWidget.topLevelItem(0).childCount()
        count2 = self.treeWidget.topLevelItem(1).childCount()
        for i in range(count1):
            self.treeWidget.topLevelItem(0).removeChild(self.treeWidget.topLevelItem(0).child(0))
        for i in range(count2):
            self.treeWidget.topLevelItem(1).removeChild(self.treeWidget.topLevelItem(1).child(0))
        # 刷新好友列表
        url = global_data.base_url + "/users/friends_and_chatroom"
        try:
            headers = {"Authorization": self.token}
            r = requests.get(url, headers=headers, proxies=global_data.proxies)
            self.loginInfo = r.json()
            # print(self.loginInfo)
        except KeyError:
            QMessageBox.warning(self, "警告", "您的用户Token无效！", QMessageBox.Yes)
            return

        for i in self.loginInfo['data']['friends']:
            # 生成item
            _item = QtWidgets.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
            # _item.setCheckState(0, Qt.Unchecked)
            _widget = ItemWidget(str(i[1]) + '（' + str(i[0]) + '）')
            self.treeWidget.setItemWidget(_item, 0, _widget)
        # 加载群聊列表
        for i in self.loginInfo['data']['chatroom_list']:
            # 生成item
            _item = QtWidgets.QTreeWidgetItem(self.treeWidget.topLevelItem(1))
            # _item.setCheckState(0, Qt.Unchecked)
            _widget = ItemWidget(str(i[1]) + '（' + str(i[0]) + '）')
            self.treeWidget.setItemWidget(_item, 0, _widget)

    # 添加好友
    def addFriend(self):
        f_id = self.friendLineEdit.text()
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
                QMessageBox.warning(self, "警告", "好友ID无效！", QMessageBox.Yes)
            # 添加成功
            else:
                QMessageBox.information(self, "提示", "添加成功！", QMessageBox.Yes)
                self.loadList()

    # 打开聊天界面
    def startChat(self, item):
        parent = item.parent()
        index_top = 0
        index_row = -1
        # 聊天码
        chatNumber = 0
        if parent is None:
            index_top = self.treeWidget.indexOfTopLevelItem(item)
        else:
            index_top = self.treeWidget.indexOfTopLevelItem(parent)
            # 获得节点在父节点中的行号(从0开始)
            index_row = parent.indexOfChild(item)
        # 打开聊天界面
        if index_row == -1:
            return
        # 好友聊天
        elif index_top == 0:
            chatNumber = self.loginInfo.get('data').get('friends')[index_row]
            self.chatWindow = ChatWindow(chatList=chatNumber, token=self.token)
            # 加载样式
            with open('../css/chatWindow.css') as file:
                qss = file.readlines()
                qss = ''.join(qss).strip('\n')
            self.chatWindow.setStyleSheet(qss)
            self.chatWindow.show()
        # 群聊
        elif index_top == 1:
            try:
                chatNumber = self.loginInfo.get('data').get('chatroom_list')[index_row]
                self.chatWindow = ChatWindow(chatList=chatNumber, token=self.token)
                # 加载样式
                with open('../css/chatWindow.css') as file:
                    qss = file.readlines()
                    qss = ''.join(qss).strip('\n')
                self.chatWindow.setStyleSheet(qss)
                self.chatWindow.show()
            except IndexError:
                QMessageBox.warning(self, "警告", "用户信息错误！", QMessageBox.Yes)
            except ValueError:
                QMessageBox.warning(self, "警告", "用户信息错误！", QMessageBox.Yes)
                return

    # 发起群聊
    def startGroup(self):
        self.groupWindow = GroupWindow(self.loginInfo['data']['friends'], self.token)
        with open('../css/startGroup.css') as file:
            qss = file.readlines()
            qss = ''.join(qss).strip('\n')
        self.groupWindow.setStyleSheet(qss)
        self.groupWindow.my_Signal.connect(self.loadList)
        self.groupWindow.show()

    # 右键菜单绑定事件
    def treeWidgetItem_fun(self, pos):
        item = self.treeWidget.currentItem()
        item1 = self.treeWidget.itemAt(pos)
        parent = item.parent()
        try:
            index_top = self.treeWidget.indexOfTopLevelItem(parent)
            index_row = parent.indexOfChild(item)
            if index_top == 0:
                if item != None and item1 != None:
                    popMenu = QMenu()
                    popMenu.addAction(QAction('查看信息', self))
                    popMenu.addAction(QAction('发送消息', self))
                    popMenu.addAction(QAction('删除好友', self))
                    popMenu.triggered[QAction].connect(self.processtrigger)
                    popMenu.exec_(QCursor.pos())
            elif index_top == 1:
                if item != None and item1 != None:
                    popMenu = QMenu()
                    popMenu.addAction(QAction('查看信息', self))
                    popMenu.addAction(QAction('发送消息', self))
                    popMenu.addAction(QAction('退出群聊', self))
                    popMenu.triggered[QAction].connect(self.processtrigger)
                    popMenu.exec_(QCursor.pos())
        # 子菜单取消右键效果
        except AttributeError:
            pass

    # 右键菜单事件处理
    def processtrigger(self, q):
        try:
            # 判断是项目节点还是任务节点
            command = q.text()
            item = self.treeWidget.currentItem()
            parent = item.parent()
            index_top = self.treeWidget.indexOfTopLevelItem(parent)
            index_row = parent.indexOfChild(item)
            # 好友
            if index_top == 0:
                if command == "发送消息":
                    self.startChat(item)
                    return
                elif command == "查看信息":
                    self.getUserInfo(index_top, index_row)
                elif command == "删除好友":
                    self.deleteFriend(self.loginInfo['data']['friends'][index_row][0])
            # 群聊
            elif index_top == 1:
                if command == "发送消息":
                    self.startChat(item)
                    return
                elif command == "查看信息":
                    self.getUserInfo(index_top, index_row)
                elif command == "退出群聊":
                    self.quitGroup(self.loginInfo['data']['chatroom_list'][index_row][0])
        except KeyError:
            return

    # 获取用户信息
    def getUserInfo(self, index_top, index_row):
        # 获取好友信息
        if index_top == 0:
            friend_url = global_data.base_url + "/users/" + str(self.loginInfo['data']['friends'][index_row][0])
            r = requests.get(url=friend_url, proxies=global_data.proxies)
            QMessageBox.information(self, "好友信息",
                                    "好友姓名 : {0}\n好友ID : {1}\n好友邮箱 : {2}".format(
                                        r.json().get('data').get('nickname'),
                                        r.json().get('data').get('id'),
                                        r.json().get('data').get('email')),
                                    QMessageBox.Yes)
        # 获取群聊信息
        elif index_top == 1:
            group_url = global_data.base_url + "/chatroom/" + str(self.loginInfo['data']['chatroom_list'][index_row][0])
            r = requests.get(url=group_url, proxies=global_data.proxies)
            member = ""
            for i in r.json().get('data').get('users'):
                member += "账号 : {0}  姓名 : {1} \n".format(i[0], i[1])
            QMessageBox.information(self, "群聊信息",
                                    "群聊名称 : {0}\n群聊ID : {1}\n创建时间 : {2}\n\n群成员 :\n{3}".format(
                                        r.json().get('data').get('name'),
                                        r.json().get('data').get('id'),
                                        datetime.now().fromisoformat(r.json().get('data').get('time')),
                                        member),
                                    QMessageBox.Yes)
            # print(r.json())

    # 删除好友
    def deleteFriend(self, friend_id):
        choice = QMessageBox.warning(self, "警告", "确定删除好友?", QMessageBox.Yes | QMessageBox.Cancel)
        if choice == QtWidgets.QMessageBox.Yes:
            url = global_data.base_url + "/users/friends"
            headers = {"Authorization": self.token}
            data = {"friend_id": friend_id}
            r = requests.delete(url=url, json=data, headers=headers)
            mes = r.json().get("mes")
            if mes:
                QMessageBox.warning(self, "警告", "删除好友失败！\n原因:{0}".format(mes), QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提醒", "删除成功！", QMessageBox.Yes)
                self.loadList()
        else:
            return

    # 退出群聊
    def quitGroup(self, group_id):
        choice = QMessageBox.warning(self, "警告", "确定退出此群聊?", QMessageBox.Yes | QMessageBox.Cancel)
        if choice == QtWidgets.QMessageBox.Yes:
            url = global_data.base_url + "/chatroom/"
            headers = {"Authorization": self.token}
            data = {"chatroom_id": group_id}
            r = requests.delete(url=url, json=data, headers=headers)
            mes = r.json().get("mes")
            if mes:
                QMessageBox.warning(self, "警告", "退出群聊失败！\n原因:{0}".format(mes), QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提醒", "退出成功！", QMessageBox.Yes)
                self.loadList()
        else:
            return

    # 程序退出
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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ListWindow({})

    with open('../css/listWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
