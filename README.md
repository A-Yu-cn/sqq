# SQQ

#### 介绍
Simple QQ是一款即时通讯软件，为本小队2021年计算机网络课程设计作品

#### 软件架构
软件架构说明

服务器: django
客户端: pyqt
消息通讯使用python socket编程


#### 使用说明

客户端为win10专用

**下载可执行程序**

1. 下载发行版sqq.zip
2. 解压
3. 运行根目录SimpleQQ.exe即可

**自己打包**

1. clone本项目

```
git clone https://gitee.com/kaichan12138/sqq.git
```

2. 打包

```
cd client
python3 -m venv venv
venv/Scripts/activate.bat
pip install -r requirements.txt
python3 build.py
```

3. 打包完成后，进入dist文件夹运行SimpleQQ.exe即可

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
