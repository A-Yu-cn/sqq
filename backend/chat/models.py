from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.CharField(null=True, max_length=255, blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField("User", null=True, blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'user'


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
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
    users = models.ManyToManyField(User, related_name="chatroom", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chatroom'