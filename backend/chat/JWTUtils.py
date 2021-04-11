import base64
from hashlib import sha256
import time
import json


class JWT(object):
    header = {
        "typ": "JWT",
        "alg": "SHA256"
    }

    play_load = {
        "iss": "sqq",  # 签发者
        "iat": "",  # 签发时间
        "jti": "",  # 身份标识
    }

    signature = ""

    salt = "sqq12138"

    @classmethod
    def get_jwt_string(cls, token):
        """获取jwt字符串"""
        cls.play_load['iat'] = str(int(time.time()))
        cls.play_load['jti'] = token
        encoded_header = base64.b64encode(json.dumps(cls.header).encode()).decode()
        encoded_play_load = base64.b64encode(json.dumps(cls.play_load).encode()).decode()
        sign = cls.get_sign(encoded_header, encoded_play_load)
        return f"{encoded_header}.{encoded_play_load}.{sign}"

    @classmethod
    def get_sign(cls, encoded_header, encoded_play_load):
        """获取签名认证信息"""
        encoded_string = f"{encoded_header}.{encoded_play_load}"
        return sha256((encoded_string + cls.salt).encode()).hexdigest()

    @classmethod
    def verify_jwt_string(cls, jwt_string: str) -> bool:
        """验证jwt字符串"""
        try:
            header, player_load, signature = jwt_string.split('.')
            return sha256(f"{header}.{player_load}{cls.salt}".encode()).hexdigest() == signature
        except Exception:
            return False
