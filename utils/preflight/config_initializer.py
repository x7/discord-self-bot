from pathlib import Path
import config
import json
import sys
import utils.logger as logger
import traceback

DEFAULT_CONFIG = {
    'discord_user_token': '',
    'discord_user_username': '',
    'discord_user_display_name': '',
    'discord_user_id': '',
    'logging': {
        'success': True,
        'warn': True,
        'info': True,
        'debug': True,
        'error': True,
        'default': True
    }
}

def initialize_config():
    app_data_directory = Path.home() / "AppData" / "Roaming"

    config_exist = does_config_exist(app_data_directory)
    if config_exist == True:
        logger.logger(log_method='debug', log_message='Config file already exists — skipping configuration creation step.')
        return
    
    logger.logger(log_method='info', log_message=f'No configuration found. Running configuration creation setup...')

    config_file = create_default_config(app_data_directory)
    if config_file == None:
        sys.exit() # exit cause we cant setup configuration file

def does_config_exist(app_data_directory):
    if Path.exists(app_data_directory / config.CONFIG_FILE_NAME):
        return True

    return False

def create_default_config(app_data_directory):
    try:
        if Path.exists(app_data_directory / config.CONFIG_FOLDER_NAME) == False:
            Path.mkdir(app_data_directory / config.CONFIG_FOLDER_NAME)

        config_file = Path(app_data_directory / config.CONFIG_FILE_NAME)
        config_file.write_text(json.dumps(obj=DEFAULT_CONFIG, indent=4), encoding='utf-8')

        logger.logger(log_method='info', log_message='Successfully created configuration file')
        return config_file
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message='Failed to create default configuration file',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )
        return None