# SQQ文档

### 账号说明

- 个人账号为5位纯数字
- 群聊账号为6位纯数字

### 部署环境

- 根url：`http://sqq.12138.site:1234`
- 后台管理：`http://sqq.12138.site:1234/admin`
  - 账号: ml   
  - 密码：0412
- socket地址：`(sqq.12138.site, 12345)`

### post请求说明

- 如果没有特别说明，所有的post请求均使用request body传输数据，格式为json
- 不支持post默认传输json格式数据的语言需要设置http headers：`content-type: application/json`
- python requests默认请求格式：`requests.post(url, json=data)`
- 除get外的其他方法默认格式同上

### 时间字符串说明

后端返回的与时间相关的信息均为iso时间字符串，例：`2021-03-17T11:48:14.944868+08:00`

将该字符串转化为datetime(python):

```python
from datetime import datetime

time_string = "2021-03-17T11:48:14.944868+08:00"
t = datetime.now().fromisoformat(time_string)
```

