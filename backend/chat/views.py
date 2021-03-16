from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *


# Create your views here.


def test(request):
    user = User.objects.get(id=12345)
    print(user.chatroom.all())
    return HttpResponse("test")
