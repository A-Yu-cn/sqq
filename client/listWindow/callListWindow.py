import sys

from client.QTreeWidget.ParsingJson import ItemWidget
from client.listWindow.listWindow import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QWidget, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy, QTreeWidget
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt


# 内嵌自定义item对象
class ItemWidget(QWidget):

    def __init__(self, text):
        super(ItemWidget, self).__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(text, self, styleSheet='color: white;font-size:20px;')
        layout.addWidget(label)
        layout.addSpacerItem(QSpacerItem(
            60, 1, QSizePolicy.Maximum, QSizePolicy.Minimum))


class ListWindow(QMainWindow, Ui_Form):

    def __init__(self, loginInfo):
        super(ListWindow, self).__init__()
        self.setupUi(self)
        # 记录登录信息
        self.treeWidget.header().setVisible(False)
        self.loginInfo = loginInfo
        self.loadList()
        # 点击父节点
        self.treeWidget.itemChanged.connect(self.handleChanged)
        # 隐藏头部
        self.treeWidget.header().setVisible(False)

    # 加载列表
    def loadList(self):
        # 加载好友列表
        pass
        for i in range(0, 10):
            # 生成item
            _item = QtWidgets.QTreeWidgetItem(self.treeWidget.topLevelItem(0))
            _item.setCheckState(0, Qt.Unchecked)
            _widget = ItemWidget("friend" + str(i))
            self.treeWidget.setItemWidget(_item, 0, _widget)
        # 加载群聊列表
        pass
        for i in range(0, 10):
            # 生成item
            _item = QtWidgets.QTreeWidgetItem(self.treeWidget.topLevelItem(1))
            _item.setCheckState(0, Qt.Unchecked)
            _widget = ItemWidget("group" + str(i))
            self.treeWidget.setItemWidget(_item, 0, _widget)

    # 父节点全选/取消全选
    def handleChanged(self, item, column):
        count = item.childCount()
        if item.checkState(column) == Qt.Checked:
            for index in range(count):
                item.child(index).setCheckState(0, Qt.Checked)
        if item.checkState(column) == Qt.Unchecked:
            for index in range(count):
                item.child(index).setCheckState(0, Qt.Unchecked)

    # def test_func(self):



if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = ListWindow({})

    with open('../css/listWindow.css') as file:
        qss = file.readlines()
        qss = ''.join(qss).strip('\n')
    myWin.setStyleSheet(qss)

    myWin.show()

    sys.exit(app.exec_())
