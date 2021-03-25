from django.test import TestCase, Client
from chat.views import *
from socket import socket
import os
import json


class UserTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.email = '1304565847@qq.com'
        self.user_id = ''
        self.login_data = ''
        self.socket = ('127.0.0.1', int(os.environ.get('TCP_SERVER_PORT')))

    def login(self, use_id=False, password='12138'):
        login_data = {
            "identity": self.email,
            "password": password
        }
        if use_id:
            login_data['identity'] = str(self.user_id)
        response = self.client.post('/users/auth', login_data, content_type='application/json')
        self.assertEqual(len(response.json()['data']['token']), 64)
        self.login_data = response.json()['data']

    def register_and_login(self):
        """测试注册之后登录"""
        register_data = {
            "email": self.email,
            "nickname": "楷禅",
            "password": "12138",
            "code": ''
        }

        # 获取验证码
        response = self.client.get('/code', {'email': self.email, 'type': 1})
        self.assertEqual(response.json().get('mes'), '')

        register_data['code'] = VerCode.objects.get(email=self.email).content
        response = self.client.post('/users/', register_data, content_type='application/json')
        self.user_id = response.json().get('data')
        # 注册成功之后用户id应该在10000~99999之间
        self.assertIn(self.user_id, range(10000, 100000))

        # 测试邮箱登录
        self.login()

        # 测试账号登录
        self.login(use_id=True)

    def get_userinfo(self):
        """"""
        response = self.client.get(f'/users/{self.user_id}')
        self.assertEqual(response.json()['data']['email'], self.email)

    def reset_password(self):
        data = {
            'email': self.email,
            'password': '12139',
            'code': ''
        }

        # 获取验证码
        response = self.client.get('/code', {'email': self.email, 'type': 2})
        self.assertEqual(response.json().get('mes'), '')

        data['code'] = VerCode.objects.get(email=self.email).content
        response = self.client.put('/users/password', data, content_type='application/json')
        self.assertEqual(response.json().get('mes'), '')

    def get_tcp_connection(self):
        client = socket()
        client.connect(self.socket)
        client.sendall(json.dumps({
            'Authorization': self.login_data.get('token')
        }).encode())
        data = json.loads(client.recv(4096))
        self.assertEqual(data.get('mes'), '')

    def test_user(self):
        self.register_and_login()
        self.get_userinfo()
        self.reset_password()
