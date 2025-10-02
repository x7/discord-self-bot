from utils.preflight import config_initializer
import utils.config_helper as config_helper
import utils.logger as logger
from pathlib import Path
import setup
import start
import utils.discord_helper as discord_helper
import time

def main():
    config_initializer.initialize_config()

    # get token value
    discord_token = config_helper.get_value('discord_user_token')
    token_check = discord_helper.get_discord_user_data(discord_token)

    if token_check['success'] == False:
        logger.logger(log_method='error', log_message='Discord token validation failed.', log_error=f'Reason: {token_check['error_message']}')
        logger.logger(log_method='info', log_message='Proceeding to run setup in 3 seconds...')
        time.sleep(3)
        return setup.setup()
    
    return start()

if __name__ == "__main__":
    main()