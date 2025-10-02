from pathlib import Path
import config
import json
import utils.logger as logger

def get_config_file():
    config_file = Path.home() / "AppData" / "Roaming" / config.CONFIG_FILE_NAME
    if Path.exists(config_file) == False:
        return None
    
    return config_file

def set_value(key, value):
    config_file = get_config_file()

    if config_file == False:
        logger.logger(log_method='warn', log_message=f'Unable to set {key} as {value} as the configuration file is null')
        return None
        
    config_object = json.loads(config_file.read_text())

    if type(config_object) != dict:
        logger.logger(log_method='error', log_message=f'Unable to set {key} as {value} as the returned config type is not a dict')
        return None
    
    does_key_exist = get_value(key)

    if does_key_exist == None:
        logger.logger(log_method='warn', log_message=f'The provided key {key} deos not exist in the config unable to set value')
        return None
    
    config_object[key] = value
    config_file.write_text(data=json.dumps(obj=config_object, indent=4), encoding='utf-8')
    logger.logger(log_method='debug', log_message=f'Set key "{key}" value to "{value}"')

def get_value(key):
    config_file = get_config_file()

    if config_file == None:
        logger.logger(log_method='warn', log_message=f'Unable to get {key} as the configuration file is null')
        return None
    
    print(config_file)

    config_object = json.loads(config_file.read_text())

    if type(config_object) != dict:
        logger.logger(log_method='warn', log_message=f'The provided key {key} deos not exist in the config unable to get value')
        return None
    
    return config_object.get(key)