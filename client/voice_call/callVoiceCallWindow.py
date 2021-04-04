from datetime import datetime
import json
import sys
import time
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QWidget, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy, QTreeWidget, QMessageBox, QMenu, QAction, QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QThread
from globalFile import GlobalData
from voice_call.voiceCall import Ui_Form

global_data = GlobalData()


class VoicePhoneWindow(QMainWindow, Ui_Form):

    def __init__(self, loginInfo):
        super(VoicePhoneWindow, self).__init__()
        self.setupUi(self)
        self.loginInfo = loginInfo


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = VoicePhoneWindow({})

    myWin.show()

    sys.exit(app.exec_())
