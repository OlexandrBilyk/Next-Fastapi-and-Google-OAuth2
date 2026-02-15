from fastapi import FastAPI, Request, Depends, Response, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from auth import create_access, create_refresh, verify_token, verify_user
import os
from db import User, get_db, AsyncSession
from sqlalchemy import select
from datetime import timedelta
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
oauth = OAuth()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account"
    }
)



@app.get('/auth/google/login')
async def google_login(req: Request):
    redirect_url = req.url_for('google_callback')
    return await oauth.google.authorize_redirect(req, redirect_url)


@app.get('/auth/google/callback')
async def google_callback(req: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(req)

    user_info = token.get('userinfo')

    if user_info:
        email = user_info.get('email')
        username = user_info.get('name')

        user = (await db.execute(select(User).where(User.email == email))).scalars().first()

        if not user:
            user = User(
                username=username,
                email=email,
                provider='google'
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)

        payload = {
            'id': user.id,
            'username': username,
            'email': email
        }

        access = create_access(payload)
        refresh = create_refresh(payload)

        res = RedirectResponse(url="http://localhost:3000/profile", status_code=status.HTTP_302_FOUND)
        
        res.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                max_age=60 * 10,
                samesite='lax',  
                secure=False,
                path='/'
            )

        res.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            max_age = 60 * 60 * 24,
            samesite='lax',  
            secure=False,
            path='/'
        )

        return res


@app.post('/auth/refresh')
def refresh(req: Request):
    refresh_token = req.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    payload = verify_token(refresh_token)

    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type')
    
    new_payload = {
        'id': payload.get('id'),
        'username': payload.get('username'),
        'email': payload.get('email')
    }

    access = create_access(new_payload)
    refresh = create_refresh(new_payload)

    res = Response()
    
    res.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            max_age=60 * 10,
            samesite='lax',  
            secure=False,
            path='/'
        )

    res.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True,
        max_age = 60 * 60 * 24,
        samesite='lax',  
        secure=False,
        path='/'
    )

    return res


@app.get('/auth/logout')
def logout():
    res = Response()
    
    res.delete_cookie(key="access_token", path='/')
    res.delete_cookie(key="refresh_token", path='/')
    
    return res


@app.get('/profile/')
def profile(user = Depends(verify_user)):
    return user

