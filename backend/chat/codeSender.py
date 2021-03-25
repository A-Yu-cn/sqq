import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os


class codeSender(object):
    def __init__(self):
        self.sender = os.environ.get('EMAIL_SENDER')
        self.passWord = os.environ.get('EMAIL_PASSWORD')
        self.smtp_server = os.environ.get('SMTP_SERVER')
        self.smtp_server_port = os.environ.get('SMTP_SERVER_PORT')
        self.s = ''
        # 邮件正文是MIMEText:

    def send(self, email, code):
        self.s = smtplib.SMTP_SSL(self.smtp_server, self.smtp_server_port)
        self.s.set_debuglevel(1)
        self.s.login(self.sender, self.passWord)
        try:
            msg = MIMEMultipart()
            # 邮件主题
            msg['Subject'] = "验证码"
            # 发送方信息
            msg['From'] = self.sender
            # QQsmtp服务器的端口号为465或587
            msg_content = f"[sqq] 您好，{code}是您的验证码，10分钟之内有效，请妥善保管"
            msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
            msg['To'] = to = email
            self.s.sendmail(self.sender, to, msg.as_string())
            return "发送成功"
        except smtplib.SMTPException:
            return "发送失败"
