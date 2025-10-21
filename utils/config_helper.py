from pathlib import Path
import platform
import os
import config
import json
import utils.log.logger as logger
import modules.setup_config as setup_config
import main
import traceback
import time
import sys

DEFAULT_CONFIG = {
    'discord_user_token': '',
    'discord_user_username': '',
    'discord_user_display_name': '',
    'discord_user_id': '',
    'discord_prefix': '!',
    'logging': {
        'success': True,
        'warn': True,
        'info': True,
        'debug': True,
        'error': True,
        'default': True
    }
}

def get_config_folder():
    system = platform.system()
    config_file_path = None

    match platform.system().lower():
        case "windows":
            config_file_path = Path.home() / "AppData" / "Roaming" / config.CONFIG_FOLDER_NAME

        case "darwin":
            config_file_path = Path.home() / "Documents" / config.CONFIG_FILE_NAME
        
        case "linux": # not supported
            return os.system('clear')
        
        case _:
            logger.logger(log_method='error', log_message=f'OS: {system} is not currently supported. Failed to get a valid config folder path')
            return None
    
    return Path(config_file_path)

def does_config_exist():
    config_file = get_config_folder() / config.CONFIG_FILE_NAME

    if config_file().exists() == True:
        return True

    return False

def get_config_file():
    config_file_path = Path(get_config_path())

    if does_config_exist() == False:
        logger.logger(log_method='info', log_message='Configuration file did not exist redirecting to configuration setup in 3 seconds...')
        time.sleep(3)
        setup_config.setup()

        return None
    
    try:
        config_file_cache = main.file_content_cache.get('config')
        if config_file_cache == None:
            config_object = json.loads(config_file_path.read_text())
            main.file_content_cache.add(key='config', value=config_object)
        else:
            config_object = config_file_cache
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message=f'The returned config was not a dict. Invalid config returned please create a new configuration file',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )

        logger.logger(log_method='info', log_message='Redirecting to configuration setup in 3 seconds...')
        time.sleep(3)
        setup_config.setup()

        return None
    
    return {
        'config_file_path': config_file_path,
        'config_file_object': config_object
    }

def create_default_config():
    config_exist = does_config_exist()
    config_path = get_config_path()
    
    if config_exist == True:
        config_path.unlink()
        
    config_path.parent.mkdir(parents=True)
    config_path.touch()
    
    try:
        config_path.write_text(json.dumps(obj=DEFAULT_CONFIG, indent=4), encoding='utf-8')
        logger.logger(log_method='success', log_message='Successfully created configuration file')
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message='Failed to create default configuration file',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )

        sys.exit()

def set_value(key, value):
    config_file = get_config_file()
    if config_file == None:
        return None

    config_file_path = config_file.get('config_file_path')
    config_file_object = config_file.get('config_file_object')

    if key not in config_file_object:
        logger.logger(log_method='warn', log_message=f'The provided key {key} does not exist in the config unable to set value')
        return None
    
    config_file_object[key] = value
    config_file_path.write_text(data=json.dumps(obj=config_file_object, indent=4), encoding='utf-8')
    logger.logger(log_method='debug', log_message=f'Set key "{key}" value to "{value}"')

    main.file_content_cache.add(key='config', value=config_file_object)

def get_value(key):
    config_file = get_config_file()
    if config_file == None:
        return None
    
    return config_file.get('config_file_object').get(key)