# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forgetPasswordWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 367)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 35, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(50, 180, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.emailLineEdit = QtWidgets.QLineEdit(Form)
        self.emailLineEdit.setGeometry(QtCore.QRect(180, 170, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.emailLineEdit.setFont(font)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.sendCodeButton = QtWidgets.QPushButton(Form)
        self.sendCodeButton.setGeometry(QtCore.QRect(310, 240, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendCodeButton.setFont(font)
        self.sendCodeButton.setObjectName("sendCodeButton")
        self.passwordLineEdit = QtWidgets.QLineEdit(Form)
        self.passwordLineEdit.setGeometry(QtCore.QRect(180, 30, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(50, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.passwordLineEdit_2 = QtWidgets.QLineEdit(Form)
        self.passwordLineEdit_2.setGeometry(QtCore.QRect(180, 100, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passwordLineEdit_2.setFont(font)
        self.passwordLineEdit_2.setObjectName("passwordLineEdit_2")
        self.codeLineEdit = QtWidgets.QLineEdit(Form)
        self.codeLineEdit.setGeometry(QtCore.QRect(180, 240, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.codeLineEdit.setFont(font)
        self.codeLineEdit.setText("")
        self.codeLineEdit.setObjectName("codeLineEdit")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(70, 250, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.registerButton = QtWidgets.QPushButton(Form)
        self.registerButton.setGeometry(QtCore.QRect(90, 310, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.registerButton.setFont(font)
        self.registerButton.setObjectName("registerButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "密码:"))
        self.label_5.setText(_translate("Form", "电子邮箱:"))
        self.sendCodeButton.setText(_translate("Form", "发送验证码"))
        self.label_4.setText(_translate("Form", "确认密码:"))
        self.label_6.setText(_translate("Form", "验证码:"))
        self.registerButton.setText(_translate("Form", "重置密码"))
