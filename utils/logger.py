import colorama
from pathlib import Path
from datetime import datetime
import utils.date_formatter as date_formatter
import config
import utils.util as util
import json
import traceback

# Find a better log way for inside these functions as it causes infinite loops
def logger(log_method, log_message, log_error = "", log_stacktrace = ""): 
    current_time = date_formatter.format_datetime(datetime.now())
    valid_log_types = ['success', 'warn', 'info', 'error', 'debug', 'default']

    if log_method.lower() not in valid_log_types:
        return logger(log_method='default', log_message=f"Invalid log type '{log_method}' provided, falling back to DEFAULT.")
    
    log_string = None
    
    match log_method.lower():
        case 'success':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.GREEN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'warn':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.YELLOW}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'info':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.CYAN}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'debug':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.BLUE}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'error':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.RED}[{log_method.upper()}]{colorama.Fore.RESET} - '
        case 'default':
            log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.WHITE}[{log_method.upper()}]{colorama.Fore.RESET} - '

    print(log_string + log_message)
    log_string = util.strip_ansi_codes(log_string + log_message)
    if log_method.lower() == 'error':
        log_string = log_string + f' | Error: {log_error} | StackTrace: {log_stacktrace}'

    log_text_file(text_file_name=log_method, log_message=log_string)
    log_json(json_file_name=log_method, log_message=log_string)

def log_text_file(text_file_name, log_message):
    text_file_folder = Path.home() / "Appdata" / "Roaming" / config.LOGS_TEXT_FOLDER_NAME

    try:
        if Path.exists(text_file_folder) == False:
            Path.mkdir(self=text_file_folder, parents=True)

        if Path.exists(text_file_folder / f'{text_file_name}.txt') == False:
            Path.write_text(self=text_file_folder / f'{text_file_name}.txt', data=f'{log_message}\n', encoding='utf-8')
            return
        
        text_file = Path(text_file_folder / f'{text_file_name}.txt')
        with text_file.open(mode='a', encoding='utf-8') as file:
            file.write(f'{log_message}\n')
    except Exception as error:
        return logger(log_method='error', log_message=f'Failed to write to {text_file_name}.txt', log_error=error, log_stacktrace=traceback.print_exc())

# Handle errors
def log_json(json_file_name, log_message):
    json_file_folder = Path.home() / "Appdata" / "Roaming" / config.LOGS_JSON_FOLDER_NAME

    if Path.exists(json_file_folder) == False:
        logger(log_method='debug', log_message=f'Path {json_file_folder} did not exist. Creating path')
        Path.mkdir(self=json_file_folder, parents=True)

    json_file = Path(json_file_folder / f'{json_file_name}.json')
    if json_file.exists() == False:
        default_json = None

        if json_file_name.lower() == 'error':
            default_json = [{
                'log_method': json_file_name.upper(),
                'log_message': log_message.split(' - ')[1].strip(),
                'log_error': log_message.split(' - ')[1].split(' | ')[1],
                'log_stacktrace': log_message.split(' - ')[1].split(' | Error: ')[1].split(' | StackTrace: ')[1]
            }]
        else:
            default_json = [{
                'log_method': json_file_name.upper(),
                'log_message': log_message.split(' - ')[1].strip(),
            }]

        json_file.write_text(data=json.dumps(obj=default_json, indent=4), encoding='utf-8')
        return
    
    with json_file.open(mode='r', encoding='utf-8') as file:
        json_string = list(json.loads(file.read()))
        new_json_object = None

        if json_file_name.lower() == 'error':
            new_json_object = {
                'log_method': json_file_name.upper(),
                'log_message': log_message.split(' - ')[1].split(' | Error: ')[0],
                'log_error': log_message.split(' - ')[1].split(' | Error: ')[1].split(' | StackTrace: ')[0],
                'log_stracktrace': log_message.split(' - ')[1].split(' | Error: ')[1].split(' | StackTrace: ')[1]
            }
        else:
            new_json_object = {
                'log_method': json_file_name.upper(),
                'log_message': log_message.split(' - ')[1].strip()
            }

        json_string.append(new_json_object)
        with json_file.open(mode="w", encoding="utf-8") as file:
            file.write(json.dumps(obj=json_string, indent=4))