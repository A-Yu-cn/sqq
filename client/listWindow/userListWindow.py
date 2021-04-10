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
        self.treeWidget.setGeometry(QtCore.QRect(0, 140, 441, 801))
        self.treeWidget.setStyleSheet("border: 0")
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.firstNameLabel = QtWidgets.QLabel(Form)
        self.firstNameLabel.setGeometry(QtCore.QRect(30, 30, 80, 80))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.firstNameLabel.setFont(font)
        self.firstNameLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.firstNameLabel.setStyleSheet("border-color: lightyellow;background-color: #FFD700;\n"
"border-radius:40px;\n"
"color: black;\n"
"")
        self.firstNameLabel.setTextFormat(QtCore.Qt.RichText)
        self.firstNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.firstNameLabel.setIndent(0)
        self.firstNameLabel.setObjectName("firstNameLabel")
        self.usernameLabel = QtWidgets.QLabel(Form)
        self.usernameLabel.setGeometry(QtCore.QRect(130, 30, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.usernameLabel.setObjectName("usernameLabel")
        self.idLabel = QtWidgets.QLabel(Form)
        self.idLabel.setGeometry(QtCore.QRect(130, 70, 81, 31))
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
        self.hideButton = QtWidgets.QPushButton(Form)
        self.hideButton.setGeometry(QtCore.QRect(320, 4, 50, 30))
        self.hideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton.setStyleSheet("")
        self.hideButton.setObjectName("hideButton")
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(330, 50, 60, 60))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.addButton.setFont(font)
        self.addButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addButton.setStyleSheet("border-radius: 30px;\n"
"border-style: outset;\n"
"background-color: #f2f5fa;\n"
"")
        self.addButton.setObjectName("addButton")

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
        self.firstNameLabel.setText(_translate("Form", "旭"))
        self.usernameLabel.setText(_translate("Form", "Pikachu"))
        self.idLabel.setText(_translate("Form", "12345"))
        self.closeButton.setText(_translate("Form", "x"))
        self.hideButton.setText(_translate("Form", "-"))
        self.addButton.setText(_translate("Form", "+"))

