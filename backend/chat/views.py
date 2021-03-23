from django.views.decorators.csrf import csrf_exempt
import json
from .utils import *
import chat.server
from itertools import chain
from datetime import datetime
from .codeSender import codeSender

code_sender = codeSender()


class UserView:

    @staticmethod
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
            'self': {
                'id': user.id,
                'nickname': user.nickname
            },
            "token": token.content,
            "friends": friends,
            "chatroom_list": chatroom_list,
            "unread_message": unread_message
        }

    @staticmethod
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

    @staticmethod
    @csrf_exempt
    def login(request):
        if request.method == "POST":
            data = json.loads(request.body)
            identity = data.get("identity")
            password = data.get("password")
            try:
                # 邮箱登录
                if "@" in identity:
                    user = User.objects.get(email=identity)
                else:
                    user = User.objects.get(id=identity)
                if user.password == parse_password(password):
                    login_data = UserView.get_login_data(user)
                    return wrap_response("", login_data)
                else:
                    return wrap_response("密码错误")
            except User.DoesNotExist:
                return wrap_response("用户不存在")
        else:
            return wrap_response('wrong method')

    @staticmethod
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

    @staticmethod
    def send_code(request):
        email = request.GET.get('email')
        ty = int(request.GET.get('type'))  # 发送验证码类型，1-注册，2-重置密码
        content = generate_code()
        now = timezone.now()
        if ty == 1:
            try:
                User.objects.get(email=email)
                return wrap_response('该邮箱已注册')
            except User.DoesNotExist:
                pass
        elif ty == 2:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return wrap_response('该邮箱未注册')
        else:
            return wrap_response('发送类型错误')
        try:
            ver_code = VerCode.objects.get(email=email)
            if (timezone.now() - ver_code.time).total_seconds() <= 60:
                return wrap_response('发送间隔太短')
            else:
                ver_code.content = content
                ver_code.time = now
        except VerCode.DoesNotExist:
            ver_code = VerCode(email=email, content=content, time=now)
        ver_code.save()
        code_sender.send(email, content)
        return wrap_response('')


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


@token_verify
def get_message(request, user):
    try:
        body = json.loads(request.body)
        other_id = int(body.get('other_id'))
        start_time = datetime.now().fromisoformat(body.get('start_time'))
        end_time = datetime.now().fromisoformat(body.get('end_time'))
    except ValueError as e:
        return wrap_response('Value error')
    # 获取用户之间的消息
    if other_id < 100000:
        other_user = User.objects.get(id=other_id)
        m1 = Message.objects.filter(to=other_id, from_user=user, createTime__gte=start_time, createTime__lte=end_time)
        m2 = Message.objects.filter(from_user=other_user, to=user.id, createTime__gte=start_time,
                                    createTime__lte=end_time)
        message_list = [{
            'from': message.from_user.id,
            'to': message.to,
            'content': message.content,
            'time': timezone.localtime(message.createTime).isoformat()
        } for message in chain(m1, m2)]
    else:
        message_list = Message.objects.filter(to=other_id, createTime__gte=start_time, createTime__lte=end_time)
    return wrap_response('', {
        'message_list': message_list
    })
