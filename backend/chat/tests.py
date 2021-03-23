from django.test import TestCase, Client
from chat.views import *
from django.http import HttpRequest
import json


class AuthTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_register_and_login(self):
        """测试注册之后登录"""
        register_data = {
            "email": "1791670972@qq.com",
            "nickname": "楷禅",
            "password": "12138"
        }
        login_data = {
            "identity": "1791670972@qq.com",
            "password": "12138"
        }
        response = self.client.post('/users/', register_data, content_type='application/json')
        user_id = response.json().get('data')
        # 注册成功之后用户id应该在10000~99999之间
        self.assertIn(user_id, range(10000, 100000))

        # 测试邮箱登录
        response = self.client.post('/users/auth', login_data, content_type='application/json')
        self.assertEqual(len(response.json()['data']['token']), 64)

        # 测试账号登录
        login_data['identity'] = str(user_id)
        response = self.client.post('/users/auth', login_data, content_type='application/json')
        self.assertEqual(len(response.json()['data']['token']), 64)
