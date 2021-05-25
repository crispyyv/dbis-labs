import uuid
from typing import Optional

import aioredis
from fastapi import FastAPI, Cookie, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from fastapi import Request
from starlette.responses import Response
from tortoise.contrib.fastapi import register_tortoise
from dotenv import dotenv_values
from database.models import User, NftToken
import datetime

from handlers.handle_get_all_tokens_from_db import get_all_tokens_from_db
from handlers.handle_get_user_tokens import get_user_tokens
from models.models_pydantic import *
from handlers.handle_create_nft import handle_create_nft
from handlers.handle_delete_user import handle_delete_user
from handlers.handle_update_user import handle_update_user
from handlers.handle_create_user import handle_create_user
from service import  get_database_user_from_credentials, get_database_user_from_cookie

app = FastAPI(
    description='Vlad Task 3',
    version='1',
    default_response_class=UJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://95.163.12.156:8998', 'https://95.163.12.156:8998'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def environment_middleware(request: Request, call_next):
    request.environments = env
    response = await call_next(request)
    return response


@app.on_event('startup')
async def startup_event():
    global env, redis
    redis = await aioredis.create_redis_pool('redis://redis')
    env = dotenv_values('.env')
    database_url = f"postgres://{env['DATABASE_USERNAME']}:{env['DATABASE_PASSWORD']}@" \
                   f"{env['DATABASE_HOST']}:5432/{env['DATABASE_NAME']}"
    register_tortoise(
        app,
        db_url=database_url,
        modules={"models": ["database.models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )


@app.exception_handler(500)
async def handle_server_error(req, exc):
    response = UJSONResponse({
        'data': None,
        'error': str(exc),
        'service_info': datetime.datetime.now().isoformat()
    }, status_code=500)
    cors_headers = CORSMiddleware(app,
                                  allow_origins=['http://95.163.12.156:8998', 'https://95.163.12.156:8998'],
                                  allow_credentials=True,
                                  allow_methods=["*"],
                                  allow_headers=["*"], ).simple_headers
    response.headers.update(cors_headers)
    return response


@app.get('/api/v1/user/')
async def get_user(user_cookie: Optional[str] = Cookie(None)):
    user = await get_database_user_from_cookie(redis, user_cookie)
    if user is None:
        return UJSONResponse({
            'data': None,
            'error': 'no such user',
            'service_info': datetime.datetime.now().isoformat()

        }, status_code=404)
    return {
        'data': user.id,
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.post('/api/v1/user/create/')
async def create_user(data: UserCreatePydantic, response: Response):
    model = User
    result = await handle_create_user(data, model)
    generated_uuid = uuid.uuid4()
    await redis.set(str(generated_uuid), result.id)
    return {
        'data': {
            'id': result.id,
            'set_cookie': {
                'key': 'user_cookie',
                'value': str(generated_uuid)
            }
        },
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.delete('/api/v1/user/')
async def delete_user(user_cookie: Optional[str] = Cookie(None)):
    user = await get_database_user_from_cookie(redis, user_cookie)
    if user is None:
        return UJSONResponse({
            'data': None,
            'error': 'no such user',
            'service_info': datetime.datetime.now().isoformat()
        }, status_code=404)
    await handle_delete_user(user)
    return {
        'data': 'success',
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.patch('/api/v1/user/')
async def update_user(data: UserMutationPydantic, user_cookie: Optional[str] = Cookie(None)):
    user = await get_database_user_from_cookie(redis, user_cookie)
    if user is None:
        return UJSONResponse({
            'data': None,
            'error': 'no such user',
            'service_info': datetime.datetime.now().isoformat()
        }, status_code=404)
    await handle_update_user(user, data.data)
    return {
        'data': 'success',
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.post('/api/v1/nft-token/create/')
async def create_nft_record(request: Request, user_cookie: Optional[str] = Cookie(None)):
    model = NftToken
    user = await get_database_user_from_cookie(redis, user_cookie)
    if user is None:
        return UJSONResponse({
            'data': None,
            'error': 'no such user',
            'service_info': datetime.datetime.now().isoformat()
        }, status_code=404)
    result = await handle_create_nft(user, model)
    return {
        'data': result,
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.get('/api/v1/nft-token/')
async def get_all_tokens(request: Request, user_cookie: Optional[str] = Cookie(None)):
    model = NftToken
    user = await get_database_user_from_cookie(redis, user_cookie)
    if user is None:
        return UJSONResponse(
            {
                'data': None,
                'error': 'no such user',
                'service_info': datetime.datetime.now().isoformat()
            }, status_code=404
        )
    result = await get_user_tokens(user, model)
    return {
        'data': result,
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }


@app.get('/api/v1/nft-token/all/')
async def get_all_tokens_in_db(request: Request):
    model = NftToken
    result = await get_all_tokens_from_db(model)
    return {
        'data': result,
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }

@app.post('/login/')
async def login(data: LoginUserModel, response: Response):
    nickname = data.nickname
    password = data.password
    user = await get_database_user_from_credentials(nickname, password)
    if user is None:
        return UJSONResponse({
            'data': None,
            'error': 'no such user',
            'service_info': datetime.datetime.now().isoformat()
        }, status_code=404)
    generate_uuid = uuid.uuid4()
    await redis.set(str(generate_uuid), user.id)
    return {
        'data': {
            'status': 'success',
            'set_cookie': {
                'key': 'user_cookie',
                'value': str(generate_uuid)
            }
        },
        'error': None,
        'service_info': datetime.datetime.now().isoformat()
    }