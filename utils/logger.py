import colorama
from datetime import datetime
import utils.date_formatter as date_formatter

def logger(log_method, log_message): 
    current_time = date_formatter.format_datetime(datetime.now())
    valid_log_types = ['success', 'warn', 'error', 'debug']

    if log_method.lower() not in valid_log_types:
        print('invalid log type provided')
        return
    
    log_string = None
    
    match log_method.lower():
        case 'success': log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.GREEN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'warn': log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.GREEN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'debug': log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.GREEN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'error': log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.GREEN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case _: '' # Error log here

    print(log_string + log_message)
    log_text_file()
    log_json()

def log_text_file():
    print('hi')

def log_json():
    print('hi')