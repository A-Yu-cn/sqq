import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAbstractItemView, QListWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ListViewDemo(QWidget):
    def __init__(self, parent=None):
        super(ListViewDemo, self).__init__(parent)
        # 设置初始大小与标题
        self.resize(300, 270)
        self.setWindowTitle('QListView 多选问题')

        # 垂直布局
        self.layout = QVBoxLayout()

        self.qList = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9',
                      'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 6', 'Item 7', 'Item 8', 'Item 9']

        self.listWidget = QListWidget(self)
        for i in self.qList:
            _item = QtWidgets.QListWidgetItem(i)
            _item.setCheckState(0)
            self.listWidget.addItem(_item)
        # self.listWidget.addItems(self.qList)  # 批量加

        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 按住CTRL可多选
        # self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)  #单选

        text_list = self.listWidget.selectedItems()
        text = [i.text() for i in list(text_list)]
        print(text)

        self.label_dqxz = QtWidgets.QLabel()
        self.label_dqxz.setText("当前选择：-")

        # 单击触发自定义的槽函数
        self.listWidget.itemClicked.connect(self.clicked)

        # 设置窗口布局，加载控件
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.label_dqxz)
        self.setLayout(self.layout)

    def clicked(self):
        text_list = self.listWidget.selectedItems()
        text = [i.text() for i in list(text_list)]
        text = '、'.join(text)  # text即多选项并以、隔开
        self.label_dqxz.setText('当前选择：' + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())
