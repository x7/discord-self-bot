import colorama
import time
import utils.config_helper as config_helper
import utils.discord_helper as discord_helper
import utils.encryption as encryption
import utils.log.logger as logger
import modules.setup_config as setup_config
import utils.util as util

def start():
    util.clear_console()
    start_message()

    discord_token = encryption.decrypt_data(config_helper.get_value('discord_user_token'))
    token_check = discord_helper.get_discord_user_data(discord_token)

    if token_check['success'] == False:
        logger.logger(log_method='error', log_message='Discord token validation failed.', log_error=f'Reason: {token_check['error_message']}')
        logger.logger(log_method='info', log_message='Proceeding to run configuration setup in 3 seconds...')
        time.sleep(3)

        return setup_config.setup()
    
    discord_username = config_helper.get_value('discord_user_username')
    discord_id = config_helper.get_value('discord_user_id')
    logger.logger(log_method='success', log_message=f'Authentication successful for user {discord_username} [ID: {discord_id}].')

def start_message():
    width = 50
    print(colorama.Fore.CYAN + "=" * width)
    print(colorama.Fore.GREEN + "Starting Discord Self Bot...".center(width))
    print(colorama.Fore.CYAN + "=" * width)