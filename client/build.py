"""
sqq构建脚本
"""

import os
import shutil

os.system('pyinstaller -F -w SimpleQQ.py')

# 复制资源文件
shutil.copytree('css', os.path.join('dist', 'css'))
shutil.copytree('emojy', os.path.join('dist', 'emojy'))
shutil.copytree('imgs', os.path.join('dist', 'imgs'))
shutil.copytree('media', os.path.join('dist', 'media'))
