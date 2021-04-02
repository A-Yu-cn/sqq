# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userListWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(436, 942)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(0, 140, 431, 801))
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.friendLineEdit = QtWidgets.QLineEdit(Form)
        self.friendLineEdit.setGeometry(QtCore.QRect(220, 40, 211, 41))
        self.friendLineEdit.setObjectName("friendLineEdit")
        self.addFriendPushButton = QtWidgets.QPushButton(Form)
        self.addFriendPushButton.setGeometry(QtCore.QRect(220, 90, 101, 41))
        self.addFriendPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addFriendPushButton.setObjectName("addFriendPushButton")
        self.startGroupPushButton = QtWidgets.QPushButton(Form)
        self.startGroupPushButton.setGeometry(QtCore.QRect(330, 90, 101, 41))
        self.startGroupPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startGroupPushButton.setObjectName("startGroupPushButton")
        self.firstNameLabel = QtWidgets.QLabel(Form)
        self.firstNameLabel.setGeometry(QtCore.QRect(10, 30, 101, 101))
        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.firstNameLabel.setFont(font)
        self.firstNameLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.firstNameLabel.setStyleSheet("border-color: lightyellow;background-color: #FFD700;\n"
"border-radius:50%;\n"
"color: black;\n"
"")
        self.firstNameLabel.setTextFormat(QtCore.Qt.RichText)
        self.firstNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.firstNameLabel.setIndent(0)
        self.firstNameLabel.setObjectName("firstNameLabel")
        self.usernameLabel = QtWidgets.QLabel(Form)
        self.usernameLabel.setGeometry(QtCore.QRect(125, 35, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.usernameLabel.setObjectName("usernameLabel")
        self.idLabel = QtWidgets.QLabel(Form)
        self.idLabel.setGeometry(QtCore.QRect(125, 65, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.idLabel.setFont(font)
        self.idLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.idLabel.setObjectName("idLabel")
        self.closeButton = QtWidgets.QPushButton(Form)
        self.closeButton.setGeometry(QtCore.QRect(380, 4, 50, 30))
        self.closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeButton.setStyleSheet("")
        self.closeButton.setObjectName("closeButton")
        self.firstNameLabel_2 = QtWidgets.QLabel(Form)
        self.firstNameLabel_2.setGeometry(QtCore.QRect(110, 100, 45, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.firstNameLabel_2.setFont(font)
        self.firstNameLabel_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.firstNameLabel_2.setStyleSheet("border-width: 1px;border-style: solid;\n"
"border-color: lightyellow;background-color:    #00FF00;\n"
"border-radius:50%;\n"
"color: black;\n"
"")
        self.firstNameLabel_2.setTextFormat(QtCore.Qt.RichText)
        self.firstNameLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.firstNameLabel_2.setIndent(0)
        self.firstNameLabel_2.setObjectName("firstNameLabel_2")
        self.firstNameLabel_3 = QtWidgets.QLabel(Form)
        self.firstNameLabel_3.setGeometry(QtCore.QRect(160, 100, 45, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.firstNameLabel_3.setFont(font)
        self.firstNameLabel_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.firstNameLabel_3.setStyleSheet("border-width: 1px;border-style: solid;\n"
"border-color: lightyellow;background-color: #F0E68C;\n"
"border-radius:50%;\n"
"color: black;\n"
"")
        self.firstNameLabel_3.setTextFormat(QtCore.Qt.RichText)
        self.firstNameLabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.firstNameLabel_3.setIndent(0)
        self.firstNameLabel_3.setObjectName("firstNameLabel_3")
        self.hideButton = QtWidgets.QPushButton(Form)
        self.hideButton.setGeometry(QtCore.QRect(320, 4, 50, 30))
        self.hideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton.setStyleSheet("")
        self.hideButton.setObjectName("hideButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget.headerItem().setText(0, _translate("Form", "用户列表"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "好友列表"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "群列表"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.friendLineEdit.setPlaceholderText(_translate("Form", "请输入好友ID"))
        self.addFriendPushButton.setText(_translate("Form", "添加好友"))
        self.startGroupPushButton.setText(_translate("Form", "发起群聊"))
        self.firstNameLabel.setText(_translate("Form", "旭"))
        self.usernameLabel.setText(_translate("Form", "Pikachu"))
        self.idLabel.setText(_translate("Form", "12345"))
        self.closeButton.setText(_translate("Form", "x"))
        self.firstNameLabel_2.setText(_translate("Form", "LV5"))
        self.firstNameLabel_3.setText(_translate("Form", "VIP"))
        self.hideButton.setText(_translate("Form", "-"))

