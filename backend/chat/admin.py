from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to')


admin.site.register(Chatroom)
admin.site.register(User)
admin.site.register(Message, MessageAdmin)
admin.site.register(Token)
admin.site.register(UnreadMessage)
admin.site.register(VerCode)
admin.site.register(File)
