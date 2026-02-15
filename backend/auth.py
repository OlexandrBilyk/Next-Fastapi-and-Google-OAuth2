from fastapi import Request, HTTPException, status
from authlib.jose.errors import ExpiredTokenError, DecodeError
from authlib.jose import jwt
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
import os

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALG = os.getenv('JWT_ALG')
HEADER = {"alg": JWT_ALG}

def create_access(data: dict) -> str:
    payload = data.copy()
    payload['type'] = 'access'
    payload['exp'] = int((datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp())

    return jwt.encode(HEADER, payload, JWT_SECRET).decode()


def create_refresh(data: dict) -> str:
    payload = data.copy()
    payload['type'] = 'refresh'
    payload['exp'] = int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())

    return jwt.encode(HEADER, payload, JWT_SECRET)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET)
        payload.validate()

        return payload
    except ExpiredTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except DecodeError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


def verify_user(request: Request) -> dict:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    data = verify_token(token)

    payload = {
        'id': data.get('id'),
        'username': data.get('username'),
        'email': data.get('email')
    }

    return payload

