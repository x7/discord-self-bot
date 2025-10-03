from utils.preflight import config_initializer
import modules.setup as setup
import modules.start as start
import colorama
import modules.view_discord_info as view_discord_info
import os

colorama.init(autoreset=True)

def main():
    os.system('cls')
    config_initializer.initialize_config()

    choices = {
        '1': 'View assigned discord account',
        '2': 'Create a new configuration',
        '3': 'Start self bot'
    }

    print_main_menu(choices)

    while True:
        input_choice = input(colorama.Fore.MAGENTA + "➜ " + colorama.Fore.YELLOW + " Enter your choice: " + colorama.Fore.WHITE)

        if input_choice in choices:
            break

        print(colorama.Fore.RED + "[!] Thats not a valid option, please choose again.")
        continue

    match input_choice.lower():
        case "1":
            return view_discord_info.view_discord_info()
        case "2":
            return setup.setup()
        case "3":
            return start.start()

def print_main_menu(choices):
    width = 40
    title = "⚡ MAIN MENU ⚡"

    print(colorama.Fore.CYAN + "=" * width)
    print(colorama.Fore.YELLOW + title.center(width))
    print(colorama.Fore.CYAN + "=" * width)

    for key, value in choices.items():
        print(colorama.Fore.GREEN + f"[{key}]" + colorama.Fore.WHITE + f" - {value}")
    print(colorama.Fore.CYAN + "=" * width)

if __name__ == "__main__":
    main()