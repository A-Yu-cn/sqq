# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addUserAndGroup.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(292, 144)
        self.idLineEdit = QtWidgets.QLineEdit(Form)
        self.idLineEdit.setGeometry(QtCore.QRect(10, 20, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.idLineEdit.setFont(font)
        self.idLineEdit.setText("")
        self.idLineEdit.setObjectName("idLineEdit")
        self.startGroupButton = QtWidgets.QPushButton(Form)
        self.startGroupButton.setGeometry(QtCore.QRect(10, 80, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startGroupButton.setFont(font)
        self.startGroupButton.setObjectName("startGroupButton")
        self.searchButton = QtWidgets.QPushButton(Form)
        self.searchButton.setGeometry(QtCore.QRect(150, 80, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.idLineEdit.setPlaceholderText(_translate("Form", "好友ID/群聊ID"))
        self.startGroupButton.setText(_translate("Form", "发起群聊"))
        self.searchButton.setText(_translate("Form", "搜索"))

