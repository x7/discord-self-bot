from pathlib import Path
import importlib
import utils.log.logger as logger
import traceback

BLACKLISTED_WORDS = ['__pycache__', 'event_handler.py']

# add mac/linux support
# fix issue if folder name has . it will replace
def load_all_events():
    events_directory = Path.cwd() / 'events'
    if events_directory.exists() == False:
        logger.logger(log_method='error', log_message='The "events" folder was not found. Not able to import/load events')
        return
    
    all_files = [file for file in events_directory.rglob('*.py') if file.name not in BLACKLISTED_WORDS]

    if len(all_files) == 0:
        logger.logger(log_method='warn', log_message='No python files found in "events" directory')
        return
    
    for file in all_files:
        module_path = str(file.absolute()).split('events')[1].replace('\\', ' ').replace('.py', ' ').strip()
        path_to_import = f'events.{module_path.replace(' ', '.')}'
        try:
            importlib.import_module(path_to_import)
        except Exception as error:
            logger.logger(
                log_method='error',
                log_message=f'Failed to import the event "{file}"',
                log_error=error,
                log_stacktrace=traceback.format_exc()
            )