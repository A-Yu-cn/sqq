from django.http import JsonResponse
from hashlib import sha256
from .models import *
import random
from django.utils import timezone


def wrap_response(mes, data=None):
    if data is None:
        data = {}
    response = JsonResponse({
        "mes": mes,
        "data": data
    })
    return response


def parse_password(password):
    halt = "12138"
    res = sha256(password.encode()).hexdigest()
    for i in range(12345):
        res = sha256(res.encode()).hexdigest()
    return res


def get_user_id():
    """生成不重复的用户id"""
    while 1:
        res = random.randint(10000, 99999)
        try:
            User.objects.get(id=res)
        except User.DoesNotExist:
            return res


def generate_token(user: User) -> Token:
    """生成token, 有效期30天"""
    try:
        token = Token.objects.get(user=user)
        if (timezone.now() - token.createTime).days >= 30:
            token.content = sha256((str(user.id) + str(random.randint(10000, 99999))).encode()).hexdigest()
            token.createTime = timezone.now()
            token.save()
    except Token.DoesNotExist:
        token = Token(user=user,
                      content=sha256((str(user.id) + str(random.randint(10000, 99999))).encode()).hexdigest(),
                      createTime=timezone.now())
        token.save()
    return token


def generate_code():
    """生成验证码"""
    return str(random.randint(100000, 999999))


def token_verify(func):
    """验证用户是否登录"""

    def wrap(request, *args, **kwargs):
        try:
            token = Token.objects.get(content=request.headers.get("Authorization"))
            if (timezone.now() - token.createTime).days >= 30:
                return wrap_response("token已过期")
        except Token.DoesNotExist:
            return wrap_response("权限验证失败")
        return func(request, *args, **kwargs, user=token.user)

    return wrap


def get_chatroom_id():
    """生成不重复的聊天室id"""
    while 1:
        res = random.randint(100000, 999999)
        try:
            Chatroom.objects.get(id=res)
        except Chatroom.DoesNotExist:
            return res


def verify_code(email, code):
    try:
        ver_code = VerCode.objects.get(email=email)
        if (timezone.now() - ver_code.time).total_seconds() >= 600:
            return '验证码已失效，请重新获取'
        return ''
    except VerCode.DoesNotExist:
        return '请先获取验证码'
