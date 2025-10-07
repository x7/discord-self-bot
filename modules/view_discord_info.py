import colorama
import os
import main
import time
import modules.setup_discord as setup_discord
import utils.config_helper as config_helper
import utils.encryption as encryption
import utils.log.logger as logger
import utils.util as util

def view_discord_info():
    util.clear_console()

    discord_token = encryption.decrypt_data(config_helper.get_value('discord_user_token'))
    if discord_token == None or discord_token == "":
        logger.logger(log_method='warn', log_message='No discord token found. Redirecting to discord setup in 3 seconds...')
        time.sleep(3)

        return setup_discord.setup_discord()
    
    discord_username = config_helper.get_value('discord_user_username')
    discord_display_name = str(config_helper.get_value('discord_user_display_name'))
    discord_id = config_helper.get_value('discord_user_id')

    discord_info_menu(
        discord_token=discord_token,
        discord_username=discord_username,
        discord_display_name=discord_display_name, 
        discord_id=discord_id
    )
    input(colorama.Fore.MAGENTA + "\nPress ENTER to return to the main menu...")

    return main.main()

def discord_info_menu(discord_token, discord_username, discord_display_name, discord_id):
    width = 50
    title = "⚡ DISCORD ACCOUNT DATA ⚡"

    print(colorama.Fore.CYAN + "=" * width)
    print(colorama.Fore.YELLOW + title.center(width))
    print(colorama.Fore.CYAN + "=" * width)

    print(colorama.Fore.GREEN + "🔑 Token: " + colorama.Fore.WHITE + discord_token)
    print(colorama.Fore.GREEN + "👤 Username: " + colorama.Fore.WHITE + discord_username)
    print(colorama.Fore.GREEN + "👤 Display Name: " + colorama.Fore.WHITE + discord_display_name)
    print(colorama.Fore.GREEN + "🆔 User ID: " + colorama.Fore.WHITE + discord_id)

    print(colorama.Fore.CYAN + "=" * width)