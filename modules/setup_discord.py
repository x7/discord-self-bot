import os
import main
import utils.log.logger as logger
import utils.discord_helper as discord_helper
import utils.config_helper as config_helper
import utils.encryption as encryption
import traceback
import colorama

def setup_discord():
    os.system('cls')
    logger.logger(log_method='info', log_message='Setting up new discord account')

    while True:
        token_input = input(f'🔑 Enter your Discord token: ').strip()
        logger.logger(log_method='info', log_message='Validating token, please wait...')

        discord_user_data = discord_helper.get_discord_user_data(token_input)
        if discord_user_data['success'] == False:
            logger.logger(
                log_method='error',
                log_message='Invalid token.',
                log_error=discord_user_data['error_message'],
                log_stacktrace=traceback.format_exc()
            )

            continue

        logger.logger(log_method='success', log_message='Valid token provided.')
        log_account_info(
            email=discord_user_data['data']['email'],
            username=discord_user_data['data']['username'],
            display_name=discord_user_data['data']['global_name'],
            user_id=discord_user_data['data']['id']
        )

        right_account = input(colorama.Fore.MAGENTA + "\n❓ Is this the correct account? (Y/N): " + colorama.Fore.WHITE).strip().lower()

        correct_answer = ['y', 'n']
        while(right_account not in correct_answer):
            right_account = input(colorama.Fore.MAGENTA + '❌ Invalid option. Please confirm with (Y/N): ' + colorama.Fore.WHITE).strip().lower()

            if right_account == 'n':
                logger.logger(log_method='info', log_message='Incorrect account token provided by the user. Restarting')
                continue

            break

        break

    # valid token
    config_helper.set_value('discord_user_token', encryption.encrypt_data(token_input))
    config_helper.set_value('discord_user_username', discord_user_data['data']['username'])
    config_helper.set_value('discord_user_display_name', discord_user_data['data']['global_name'])
    config_helper.set_value('discord_user_id', discord_user_data['data']['id'])
    logger.logger(log_method='info', log_message='Discord data saved to configuration file.')
    input(colorama.Fore.MAGENTA + "\nPress ENTER to return to the main menu...")
    
    return main.main()

def log_account_info(email, username, display_name, user_id):
    print(colorama.Fore.CYAN + "=" * 50)
    print(colorama.Fore.YELLOW + "⚡ DISCORD ACCOUNT INFO ⚡".center(50))
    print(colorama.Fore.CYAN + "=" * 50)

    print(colorama.Fore.GREEN + "📧 Email: " + colorama.Fore.WHITE + email)
    print(colorama.Fore.GREEN + "👤 Username: " + colorama.Fore.WHITE + username)
    print(colorama.Fore.GREEN +"👤 Display Name: " + colorama.Fore.WHITE + str(display_name)) # could be null
    print(colorama.Fore.GREEN + "🆔 ID: " + colorama.Fore.WHITE + user_id)

    print(colorama.Fore.CYAN + "=" * 50)