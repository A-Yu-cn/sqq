"""
sqq构建脚本
"""

import os
import shutil
import logging

logging.basicConfig(level="INFO")


class Build(object):

    def __init__(self):
        self.start_name = 'SimpleQQ.py'  # 入口程序名称
        self.static_dirs = [
            'css', 'emojy', 'imgs', 'media'
        ]

    def deal_static_files(self):
        # 尝试删除旧静态文件并复制现版本文件夹
        for static_dir in self.static_dirs:
            try:
                shutil.rmtree(os.path.join('dist', static_dir))
                shutil.copytree(static_dir, os.path.join('dist', static_dir))
                logging.info(f'delete & copy {static_dir} successfully')
            except FileNotFoundError:
                shutil.copytree(static_dir, os.path.join('dist', static_dir))
                logging.info(f'copy {static_dir} successfully')
                continue
            except Exception as e:
                logging.error(e)

    def run_build(self):
        os.system(f'pyinstaller -F -w -i imgs/chat.ico {self.start_name}')

    def run(self):
        self.run_build()
        self.deal_static_files()


if __name__ == '__main__':
    builder = Build()
    builder.run()
