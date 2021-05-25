from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

from database.models import User

UserCreatePydantic = pydantic_model_creator(User, exclude=('created_at', 'updated_at', 'id'))


class NFTTokenCreatePydantic(BaseModel):
    user_id: int


class UserMutationPydantic(BaseModel):
    user_id: int
    data: dict


class DeleteUserPydantic(BaseModel):
    user_id: int


class LoginUserModel(BaseModel):
    nickname: str
    password: str
