import os
import main
import time
import utils.log.logger as logger
import utils.config_helper as config_helper

def setup_config():
    os.system('cls')
    logger.logger(log_method='info', log_message='Starting configuration setup...')
    config_helper.create_default_config()
    logger.logger(log_method='info', log_message='Returning to main menu in 3 seconds...')
    time.sleep(3)

    return main.main()
