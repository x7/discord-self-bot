import sys
import time
import platform
import config
import utils.log.logger as logger

def check_if_system_supported():
    system = platform.system()
    supported_versions = config.SUPPORTED_OS_VERSIONS

    if system.lower() not in supported_versions:
        logger.logger(log_method='error', log_message=f'Your current OS "{system}" is not currently supported. Exiting program in 3 seconds...') 
        time.sleep(3)

        return sys.exit()