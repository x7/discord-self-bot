import os
import time
import utils.logger as logger
import utils.discord_helper as discord_helper
import utils.config_helper as config_helper
import start

def setup():
    os.system('cls')
    logger.logger(log_method='info', log_message='Starting configuration setup...')

    working_token = False
    while(working_token == False):
        token_input = input(f'🔑 Enter your Discord token: ').strip()
        logger.logger(log_method='info', log_message='Validating token, please wait...')

        discord_user_data = discord_helper.get_discord_user_data(token_input)
        if discord_user_data['success'] == False:
            logger.logger(log_method='error', log_message='Invalid token.', log_error=discord_user_data['error_message'])
            continue

        logger.logger(log_method='success', log_message='Valid token provided.')
        logger.logger(log_method='info', log_message=f'Email: {discord_user_data['data']['email']}')
        logger.logger(log_method='info', log_message=f'Username: {discord_user_data['data']['username']}')
        logger.logger(log_method='info', log_message=f'ID: {discord_user_data['data']['id']}')
        right_account = input('Is this the correct account? (Y/N): ').strip().lower()

        while(right_account != 'y' and right_account != 'n'):
            right_account = input('Invalid choice. Please enter (Y/N): ').strip().lower()

        if right_account == 'n':
            logger.logger(log_method='info', log_message='Incorrect account token provided by the user. Restarting')
            continue

        working_token = True

    # valid token
    config_helper.set_value('discord_user_token', token_input)
    logger.logger(log_method='info', log_message='Token saved to configuration file. Returning to main process in 3 seconds...')
    time.sleep(3)   
    return start.start()