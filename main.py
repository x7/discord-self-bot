import colorama
import os
import utils.util as util
import modules.setup_config as setup_config
import modules.start as start
import modules.view_discord_info as view_discord_info
import modules.setup_discord as setup_discord
import utils.file_cache as file_cache
import preflight.library_check as library_check
import preflight.version_check as version_check
import preflight.system_check as system_check

# Instances
file_content_cache = file_cache.FileCache()

CHOICES = {
    '1': 'View assigned discord account',
    '2': 'Setup discord account',
    '3': 'Create a new configuration',
    '4': 'Start self bot'
}

def main():
    util.clear_console()
    print_main_menu()

    while True:
        input_choice = input(colorama.Fore.MAGENTA + "➜ " + colorama.Fore.YELLOW + " Enter your choice: " + colorama.Fore.WHITE)

        if input_choice in CHOICES:
            break

        print(colorama.Fore.RED + "[!] Thats not a valid option, please choose again.")
        continue

    match input_choice.lower():
        case "1":
            return view_discord_info.view_discord_info()
        case "2":
            return setup_discord.setup_discord()
        case "3":
            return setup_config.setup_config()
        case "4":
            return start.start()

def print_main_menu():
    width = 40
    title = "⚡ MAIN MENU ⚡"

    print(colorama.Fore.CYAN + "=" * width)
    print(colorama.Fore.YELLOW + title.center(width))
    print(colorama.Fore.CYAN + "=" * width)

    for key, value in CHOICES.items():
        print(colorama.Fore.GREEN + f"[{key}]" + colorama.Fore.WHITE + f" - {value}")
    print(colorama.Fore.CYAN + "=" * width)

if __name__ == "__main__":
    colorama.init(autoreset=True)

    # preflight checks
    system_check.check_if_system_supported()
    version_check.validate_python_version()
    library_check.check_libraries()

    # main()