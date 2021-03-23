# 代码行数统计工具
import os
import time
from prettytable import PrettyTable as pt


# 统计项目代码数量
class TotalCodeLines():
    def __init__(self, basedir, filetype):
        self.basedir = basedir
        self.filelists = []
        self.filetype = filetype
        self.table = pt()
        self.table.field_names = ['file_path_and_name', 'lines']
        # self.table.padding_width = 1
        self.table.hrules = True  # 显示表格行边

    # 遍历文件, 递归遍历文件夹中的所有
    def readfile(self, basedir, filetype):
        global filelists
        for parent, dirnames, filenames in os.walk(self.basedir):
            for filename in filenames:
                ext = filename.split('.')[-1]
                # 只统计指定的文件类型，略过一些log和cache文件
                if ext in self.filetype:
                    self.filelists.append(os.path.join(parent, filename))
        return self.filelists

    # 统计一个文件的行数
    def countline(self, fname):
        count = 0
        for file_line in open(fname, 'rb').readlines():
            count += 1
        self.table.add_row([fname, count])
        # print('{0} {1}'.format(count, 'lines') + fname + ' ----')
        return count

    # 统计所有文件的代码行数
    def alllines(self, filelists):
        totalline = 0
        for filelist in filelists:
            totalline = totalline + self.countline(filelist)
        print(self.table)
        return totalline


if __name__ == '__main__':
    start_time = time.time()
    # 需要统计的文件夹或者文件
    basedir = r'./'
    # 指定想要统计的文件类型
    filetype = [
        'py',
        # 'js',
        # 'css',
        # 'html',
    ]
    # 调用类
    totalline = TotalCodeLines(basedir, filetype)
    file = totalline.readfile(basedir, filetype)
    totalline = totalline.alllines(file)
    print('total lines: {0} {1}'.format(totalline, 'lines'))

    end_time = time.time()
    print('Cost Time: %0.2f seconds' % (end_time - start_time))
