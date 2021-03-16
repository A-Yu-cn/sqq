from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *

# Create your views here.


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        nickname = data.get("nickname")
        password = data.get("password")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            user_id = get_user_id()
            user = User(id=user_id, email=email, nickname=nickname, password=parse_password(password))
            user.save()
            return wrap_response("", user_id)
        return wrap_response("该邮箱已注册")
    else:
        return wrap_response("请求方法错误")


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        identity = data.get("identity")
        password = data.get("password")
        try:
            if "@" in identity:
                user = User.objects.get(email=identity)
            else:
                user = User.objects.get(id=identity)
            if user.password == parse_password(password):
                return wrap_response("", "login success")
            else:
                return wrap_response("密码错误")
        except User.DoesNotExist:
            return wrap_response("用户不存在")
