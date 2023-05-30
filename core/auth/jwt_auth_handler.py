# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

import jwt

import sys
import os


# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project's root directory to sys.path
sys.path.insert(0, project_root)

from configs.config import settings



JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str, role_id: str=None) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "role": role_id,
        "expires": time.time() + 2400
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}