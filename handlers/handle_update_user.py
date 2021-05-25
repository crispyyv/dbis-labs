

async def handle_update_user(user, data):
    await user.update_from_dict(data)