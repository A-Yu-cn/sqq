# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'voiceCall.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(310, 492)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 40, 210, 210))
        font = QtGui.QFont()
        font.setPointSize(70)
        self.label.setFont(font)
        self.label.setStyleSheet("border-color: lightyellow;background-color: #FFD700;\n"
"border-radius:100%;\n"
"color: black;\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(100, 330, 111, 111))
        self.pushButton.setStyleSheet("border-radius: 50px;\n"
"border-style: outset;\n"
"background-color: red;\n"
"border-image: url(imgs/phone.png)")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "韩"))

