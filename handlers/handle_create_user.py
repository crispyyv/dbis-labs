

async def handle_create_user(data, model):
    result = await model.create(**data.dict())
    return result