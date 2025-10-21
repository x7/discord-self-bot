import user
import utils.config_helper as config_helper
import utils.discord_helper as discord_helper

@user.client.event
async def on_message(message):
    message_author_id = message.author.id

    if message_author_id != user.client.user.id:
        return
    
    prefix = config_helper.get_value('discord_prefix')
    if prefix == None or prefix == "":
        config_helper.set_value('discord_prefix', '!')
        no_prefix_found = await message.channel.send('No prefix is found in the config. Defaulting prefix to "!"')
        await discord_helper.delete_message(no_prefix_found, 3)

        return
    
    if message.content[0] != prefix or message.content[1] == None:
        return
    
    command_arguments = message.content.split(prefix)[1].split(' ')

    # command handler.
    
