import sys
import config
import time
import utils.log.logger as logger

def validate_python_version():
    current_python_version = get_python_version()
    readable_python_version = tuple(map(int, current_python_version['version'].replace('.', '')))
    recommended_version = tuple(map(int, config.RECOMMENDED_PYTHON_VERSION.replace('.', '')))

    if readable_python_version >= recommended_version:
        logger.logger(log_method='info', log_message='Python version check completed - You are currently up to date.')
        return
    
    logger.logger(log_method='warn', log_message=f'Current Python version {current_python_version['version']} is less than the recommended {config.RECOMMENDED_PYTHON_VERSION}.')
    logger.logger(log_method='info', log_message=f'Please download the latest version from https://www.python.org/downloads/ then rerun the program')
    logger.logger(log_method='info', log_message='Exiting program in 3 seconds...')
    time.sleep(3)

    return sys.exit()

def get_python_version():
    return {
        'version': sys.version.split(' (')[0],
        'full_version': sys.version
    }