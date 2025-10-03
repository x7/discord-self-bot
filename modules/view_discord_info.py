import colorama
import os
import main
import utils.config_helper as config_helper

def view_discord_info():
    os.system('cls')

    discord_token = config_helper.get_value('discord_user_token')
    discord_username = config_helper.get_value('discord_user_username') or None
    discord_display_name = config_helper.get_value('discord_user_display_name')
    discord_id = config_helper.get_value('discord_user_id')

    discord_info_menu(discord_token=discord_token, discord_username=discord_username, discord_display_name=discord_display_name, discord_id=discord_id)
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