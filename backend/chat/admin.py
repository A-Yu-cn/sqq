from django.contrib import admin
from .models import *

admin.site.register(Chatroom)
admin.site.register(User)
admin.site.register(Message)