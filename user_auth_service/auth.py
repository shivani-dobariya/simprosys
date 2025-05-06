import time
from typing import Dict

import jwt

from main import JWT_SECRET,auth_expire_time, refresh_expire_time


def create_jwt(user_id,exp_time):
    try:
        payload = {
            "user_id": user_id,
            "expires": exp_time
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token
    except Exception as e:
        return {}



def create_token(user_id: str) -> Dict[str, str]:
    try:
        return {
            "access_token": create_jwt(user_id=user_id,exp_time=auth_expire_time),
            "refresh_token": create_jwt(user_id=user_id,exp_time=refresh_expire_time),
        }
    except Exception as e:
        return {}


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
