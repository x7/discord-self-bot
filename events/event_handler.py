from pathlib import Path
import importlib
import utils.log.logger as logger

BLACKLISTED_WORDS = ['__pycache__', 'event_handler.py']

def load_all_events():
    events_directory = Path.cwd() / 'events'
    if events_directory.exists() == False:
        logger.logger(log_method='error', log_message='The "events" folder was not found. Not able to import/load events')
        return
    
    directories = [item for item in events_directory.iterdir() if item.is_dir()]
    if len(directories) == 0:
        logger.logger(log_method='warn', log_message='No subdirectories found in "events" folder.')
        return

    def read_dir(directory_path):
        for directory in directory_path:
            if any(word in str(directory.absolute()) for word in BLACKLISTED_WORDS):
                continue

            if directory.is_file() == False:
                new_directory = [new_item for new_item in directory.iterdir()]
                read_dir(directory_path=new_directory)
                continue

            path_list = str(directory.absolute()).split('\\')
            events_index = path_list.index('events')

            for num in reversed(range(events_index + 1)):
                path_list.pop(num)

            if path_list[-1].find('.py') != -1:
                path_list[-1] = path_list[-1].replace('.py', '')

            path_to_import = f'events.{".".join(path_list)}'
            importlib.import_module(path_to_import)

    read_dir(directory_path=directories)