from pathlib import Path
import config
import json

def get_config_file():
    try:
        config_file = Path.home() / "AppData" / "Roaming" / config.CONFIG_FOLDER_NAME / config.CONFIG_FILE_NAME
        return config_file
    except Exception as error:
        print(error)
        return None

def set_value(key, value):
    config_file = get_config_file()

    if config_file == None:
        print('Unable to set value as the config file is null')
        
    config_object = json.loads(config_file.read_text())

    if type(config_object) != dict:
        print('Invalid config file type')
        return None
    
    does_key_exist = get_value(key)

    if does_key_exist == None:
        print(f'Invalid key provided {key}')
        return None
    
    config_object[key] = value
    config_file.write_text(data=json.dumps(obj=config_object, indent=4), encoding='utf-8')

def get_value(key):
    config_file = get_config_file()

    if config_file == None:
        print('Unable to get value as the config file is null')

    config_object = json.loads(config_file.read_text())

    if type(config_object) != dict:
        print('Invalid config file type')
        return None
    
    return config_object.get(key)