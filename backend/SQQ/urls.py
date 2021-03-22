"""SQQ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", register),
    path("users/auth", login),
    path("users/friends", add_friend),
    path("users/<userid>", get_userinfo),
    path("chatroom/", create_chatroom),
    path("chatroom/<room_id>", get_chatroom_info),
    path('message', get_message),
    path('code', send_code),
]
