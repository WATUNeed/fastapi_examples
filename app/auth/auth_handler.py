import time

import jwt


JWT_SECRET = '1111'
JWT_ALGORITHM = 'HS256'


def encode_jwt(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
