import user

@user.client.event
async def on_ready():
    print(f'Logged in as {user.client.user.name}')
    print('Self-bot is ready.')

