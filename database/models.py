from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.validators import MinLengthValidator, MaxLengthValidator
from uuid import uuid4


def generate_hash():
    return uuid4()


class User(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    id = fields.IntField(pk=True)
    nickname = fields.CharField(unique=True, max_length=255)
    password = fields.TextField()

    def __str__(self):
        return self.nickname


class NftToken(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(f'models.User', related_name='tokens')
    hash = fields.TextField(validators=[MinLengthValidator(min_length=36), MaxLengthValidator(max_length=36)],
                            default=generate_hash)