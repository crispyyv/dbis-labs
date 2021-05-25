

async def get_user_tokens(user, model):
    tokens = await model.filter(user=user).all()
    return [token.hash for token in tokens]
