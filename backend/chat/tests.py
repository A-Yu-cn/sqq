from django.test import TestCase, Client
from chat.views import *


class UserTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user_id = ''
        self.login_data = ''

    def login(self, use_id=False, password='12138'):
        login_data = {
            "identity": "1791670972@qq.com",
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
            "email": "1791670972@qq.com",
            "nickname": "楷禅",
            "password": "12138",
            "code": ''
        }

        # 获取验证码
        response = self.client.get('/code', {'email': '1791670972@qq.com', 'type': 1})
        self.assertEqual(response.json().get('mes'), '')

        register_data['code'] = VerCode.objects.get(email='1791670972@qq.com').content
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
        self.assertEqual(response.json()['data']['email'], '1791670972@qq.com')

    def reset_password(self):
        data = {
            'email': '1791670972@qq.com',
            'password': '12139',
            'code': ''
        }

        # 获取验证码
        response = self.client.get('/code', {'email': '1791670972@qq.com', 'type': 2})
        self.assertEqual(response.json().get('mes'), '')

        data['code'] = VerCode.objects.get(email='1791670972@qq.com').content
        response = self.client.put('/users/password', data, content_type='application/json')
        self.assertEqual(response.json().get('mes'), '')

    def test_user(self):
        self.register_and_login()
        self.get_userinfo()
        self.reset_password()
