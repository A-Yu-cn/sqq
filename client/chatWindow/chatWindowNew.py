# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatWindowNew.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1119, 767)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 560, 851, 141))
        self.textEdit.setObjectName("textEdit")
        self.historyButton = QtWidgets.QPushButton(Form)
        self.historyButton.setGeometry(QtCore.QRect(760, 710, 101, 41))
        self.historyButton.setObjectName("historyButton")
        self.clearButton = QtWidgets.QPushButton(Form)
        self.clearButton.setGeometry(QtCore.QRect(540, 710, 101, 41))
        self.clearButton.setObjectName("clearButton")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(869, 10, 241, 731))
        self.widget.setObjectName("widget")
        self.historyTextBrowser = QtWidgets.QTextBrowser(self.widget)
        self.historyTextBrowser.setGeometry(QtCore.QRect(0, 0, 241, 531))
        self.historyTextBrowser.setObjectName("historyTextBrowser")
        self.dateTimeEdit_1 = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit_1.setGeometry(QtCore.QRect(0, 560, 194, 22))
        self.dateTimeEdit_1.setObjectName("dateTimeEdit_1")
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(0, 610, 194, 22))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.queryHistoryButton = QtWidgets.QPushButton(self.widget)
        self.queryHistoryButton.setGeometry(QtCore.QRect(0, 650, 101, 41))
        self.queryHistoryButton.setObjectName("queryHistoryButton")
        self.submitButton = QtWidgets.QPushButton(Form)
        self.submitButton.setGeometry(QtCore.QRect(430, 710, 101, 41))
        self.submitButton.setObjectName("submitButton")
        self.richTextButton = QtWidgets.QPushButton(Form)
        self.richTextButton.setGeometry(QtCore.QRect(650, 710, 101, 41))
        self.richTextButton.setObjectName("richTextButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(740, 530, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #888;")
        self.label.setObjectName("label")
        self.recordLabel = QtWidgets.QLabel(Form)
        self.recordLabel.setGeometry(QtCore.QRect(120, 530, 61, 16))
        self.recordLabel.setObjectName("recordLabel")
        self.recordButton = QtWidgets.QPushButton(Form)
        self.recordButton.setGeometry(QtCore.QRect(10, 520, 101, 35))
        self.recordButton.setObjectName("recordButton")
        self.cancleButton = QtWidgets.QPushButton(Form)
        self.cancleButton.setGeometry(QtCore.QRect(170, 520, 101, 35))
        self.cancleButton.setObjectName("cancleButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.historyButton.setText(_translate("Form", "历史记录"))
        self.clearButton.setText(_translate("Form", "清空"))
        self.queryHistoryButton.setText(_translate("Form", "查询"))
        self.submitButton.setText(_translate("Form", "发送"))
        self.richTextButton.setText(_translate("Form", "富文本编辑器"))
        self.label.setWhatsThis(_translate("Form", "<html><head/><body><p>color:red;</p></body></html>"))
        self.label.setText(_translate("Form", "Ctrl+Enter快速发送"))
        self.recordLabel.setText(_translate("Form", "00:00"))
        self.recordButton.setText(_translate("Form", "发送语音"))
        self.cancleButton.setText(_translate("Form", "取消发送"))

