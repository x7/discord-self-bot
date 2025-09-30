from pathlib import Path
import config
import json
import sys

DEFAULT_CONFIG = {
    'discord_user_token': '',
    'discord_user_id': ''
}

def initialize_config():
    app_data_directory = Path.home() / "AppData" / "Roaming"

    config_exist = does_config_exist(app_data_directory)
    if config_exist == True:
        print('Config exist skipping creation')
        return

    config_file = create_default_config(app_data_directory)
    if config_file == None:
        print('Error creating config file exiting program')
        sys.exit()

def does_config_exist(app_data_directory):
    if Path.exists(app_data_directory / config.CONFIG_FOLDER_NAME / config.CONFIG_FILE_NAME):
        return True

    return False

def create_default_config(app_data_directory):
    try:
        if Path.exists(app_data_directory / config.CONFIG_FOLDER_NAME) == False:
            Path.mkdir(app_data_directory / config.CONFIG_FOLDER_NAME)

        config_file = Path(app_data_directory / config.CONFIG_FOLDER_NAME / config.CONFIG_FILE_NAME)
        config_file.write_text(json.dumps(obj=DEFAULT_CONFIG, indent=4), encoding='utf-8')

        return config_file
    except Exception as error:
        print(error)
        return None