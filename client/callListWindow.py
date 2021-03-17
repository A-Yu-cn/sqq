import sys

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .listWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class ListWindow(QMainWindow, Ui_Form):

    def __init__(self):
        super(ListWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ListWindow()

    myWin.show()

    sys.exit(app.exec_())
