from uuid import uuid4
from database.models import User


async def get_database_user_from_cookie(redis, user_cookie):
    user_id = await redis.get(user_cookie)
    if user_id is None:
        return None
    user = await User.filter(id=user_id).get_or_none()
    return user


async def get_database_user_from_credentials(nickname, password):
    user = await User.filter(nickname=nickname, password=password).get_or_none()
    return user