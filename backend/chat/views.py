from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *


def get_login_data(user):
    token = generate_token(user)
    friends = [(i.id, i.nickname) for i in user.friends.all()]
    friends += [(i.id, i.nickname) for i in user.friends_set.all()]
    friends = list(set(friends))
    chatroom_list = [(i.id, i.name) for i in user.chatroom.all()]
    unread_message_db = user.unread.all()
    unread_message = [
        {
            "from": (u_message.message.from_user.id, u_message.message.from_user.nickname),
            "to": u_message.message.to,
            "content": u_message.message.content,
            "time": timezone.localtime(u_message.message.createTime).isoformat()
        }
        for u_message in unread_message_db
    ]
    unread_message_db.delete()
    return {
        "token": token.content,
        "friends": friends,
        "chatroom_list": chatroom_list,
        "unread_message": unread_message
    }


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
                login_data = get_login_data(user)
                return wrap_response("", login_data)
            else:
                return wrap_response("密码错误")
        except User.DoesNotExist:
            return wrap_response("用户不存在")


def get_userinfo(request, userid):
    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        return wrap_response("wrong id")
    return wrap_response("", {
        "id": user.id,
        "nickname": user.nickname,
        "email": user.email
    })


@csrf_exempt
@token_verify
def add_friend(request, user):
    if request.method == "POST":
        friend_id = json.loads(request.body).get("friend_id")
        try:
            friend = User.objects.get(id=friend_id)
            user.friends.add(friend)
            return wrap_response("")
        except User.DoesNotExist:
            return wrap_response("wrong friend_id")
    else:
        return wrap_response("wrong method")


@csrf_exempt
@token_verify
def create_chatroom(request, user):
    if request.method == "POST":
        data = json.loads(request.body)
        friend_ids = data.get("friend_ids")
        chatroom_name = data.get("name")
        wrong_ids = []
        chatroom = Chatroom(id=get_chatroom_id(), name=chatroom_name, createTime=timezone.now())
        chatroom.save()
        chatroom.users.add(user)
        for friend_id in friend_ids:
            try:
                chatroom.users.add(User.objects.get(id=friend_id))
            except User.DoesNotExist:
                wrong_ids.append(friend_ids)
        return wrap_response("", {
            "wrong ids": wrong_ids,
            "room_id": chatroom.id
        })
    else:
        return wrap_response("wrong method")


def get_chatroom_info(request, room_id):
    try:
        chatroom = Chatroom.objects.get(id=room_id)
        return wrap_response("", {
            "name": chatroom.name,
            "id": chatroom.id,
            "time": timezone.localtime(chatroom.createTime).isoformat(),
            "users": [(i.id, i.nickname) for i in chatroom.users.all()]
        })
    except Chatroom.DoesNotExist:
        return wrap_response("wrong id")
