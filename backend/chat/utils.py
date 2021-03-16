from django.http import JsonResponse
from hashlib import sha256
from .models import User
import random


def wrap_response(mes, data=None):
    if data is None:
        data = {}
    response = JsonResponse({
        "mes": mes,
        "data": data
    })
    if mes:
        response.status_code = 500
    return response


def parse_password(password):
    halt = "12138"
    res = sha256(password.encode()).hexdigest()
    for i in range(12345):
        res = sha256(res.encode()).hexdigest()
    return res


def get_user_id():
    while 1:
        res = random.randint(10000, 99999)
        try:
            User.objects.get(id=res)
        except User.DoesNotExist:
            return res
