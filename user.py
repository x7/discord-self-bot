import logging
from discord.ext import commands
import events.event_handler as event_handler
import utils.encryption as encryption
import utils.config_helper as config_helper

client = commands.Bot(command_prefix='!', self_bot=True)

def client_setup():
    event_handler.load_all_events()

    # disable all discord logging
    logging.getLogger('discord').setLevel(logging.CRITICAL)
    logging.getLogger('discord.client').setLevel(logging.CRITICAL)
    logging.getLogger('discord.http').setLevel(logging.CRITICAL)
    logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)

    discord_token = encryption.decrypt_data(config_helper.get_value('discord_user_token'))
    client.run(discord_token)

def get_client():
    return client