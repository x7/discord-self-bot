import os
import platform
import re
import utils.log.logger as logger

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    
    return ansi_escape.sub('', text)

def clear_console():
    system = platform.system()

    match platform.system().lower():
        case "windows":
            return os.system('cls')
        
        case "linux" | "darwin":
            return os.system('clear')
        
        case _:
            logger.logger(log_method='error', log_message=f'OS: {system} is not currently supported. Failed to clear console')
            return None