

async def get_all_tokens_from_db(model):
    result = await model.all()
    return result