from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.CharField(null=True, max_length=255, blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField("User", blank=True, related_name="friends_set")

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'user'


class Message(models.Model):
    from_user = models.ForeignKey(User, models.CASCADE)
    to = models.IntegerField()
    content = models.TextField()
    createTime = models.DateTimeField()

    def __str__(self):
        return self.from_user.nickname

    class Meta:
        db_table = 'message'


class Chatroom(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    createTime = models.DateTimeField()
    users = models.ManyToManyField(User, related_name="chatroom", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chatroom'


class Token(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, related_name="token")
    content = models.CharField(max_length=255)
    createTime = models.DateTimeField()

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = 'token'


class UnreadMessage(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="unread")
    message = models.ForeignKey(Message, models.CASCADE, related_name="unread")

    def __str__(self):
        return self.user.nickname

    class Meta:
        db_table = 'unread_message'


class VerCode(models.Model):
    content = models.CharField(max_length=6)
    time = models.DateTimeField()
    email = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'ver_code'
