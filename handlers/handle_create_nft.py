

async def handle_create_nft(user, model):
    result = await model.create(user=user)
    return result.hash
