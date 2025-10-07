import colorama
from pathlib import Path
from datetime import datetime
import utils.date_formatter as date_formatter
import config
import utils.util as util
import utils.log.generate_reference_code as generate_reference_code
import json
import traceback
import utils.config_helper as config_helper
import sys

# TODO:
# Find a better log way for inside these functions as it causes infinite loops
def logger(log_method, log_message, log_error = "", log_stacktrace = ""): 
    current_time = date_formatter.format_datetime(datetime.now())
    valid_log_types = ['success', 'warn', 'info', 'error', 'debug', 'default']
    reference_id = generate_reference_code.generate_reference_code()

    if log_method.lower() not in valid_log_types:
        return logger(log_method='default', log_message=f"Invalid log type '{log_method}' provided, falling back to DEFAULT.")
    
    log_string = f'{colorama.Fore.YELLOW}[{current_time}] {colorama.Fore.RESET}{colorama.Fore.LIGHTCYAN_EX}[Reference ID: {reference_id}]{colorama.Fore.RESET} %color%[{log_method.upper()}]{colorama.Fore.RESET} - '
    
    match log_method.lower():
        case 'success':
            log_string = log_string.replace('%color%', colorama.Fore.GREEN)
        case 'warn':
            log_string = log_string.replace('%color%', colorama.Fore.YELLOW)
        case 'info':
            log_string = log_string.replace('%color%', colorama.Fore.CYAN)
        case 'debug':
            log_string = log_string.replace('%color%', colorama.Fore.BLUE)
        case 'error':
            log_string = log_string.replace('%color%', colorama.Fore.RED)
        case 'default':
            log_string = log_string.replace('%color%', colorama.Fore.WHITE)

    print(log_string + log_message)

    log_string = util.strip_ansi_codes(log_string + log_message)
    if log_method.lower() == 'error':
        log_string = log_string + f' | Error: {log_error} | StackTrace: {log_stacktrace}'

    log_text_file(text_file_name=log_method, log_message=log_string)
    log_json(json_file_name=log_method, log_message=log_string, reference_id=reference_id, time_stamp=datetime.now().timestamp())

    return reference_id

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
        return logger(
            log_method='error',
            log_message=f'Failed to write to {text_file_name}.txt',
            log_error=error,
            log_stacktrace=traceback.print_exc()
        )

# Handle errors
def log_json(json_file_name, log_message, reference_id, time_stamp):
    json_file_folder = Path.home() / "Appdata" / "Roaming" / config.LOGS_JSON_FOLDER_NAME

    if Path.exists(json_file_folder) == False:
        logger(log_method='debug', log_message=f'Path {json_file_folder} did not exist. Creating path')
        Path.mkdir(self=json_file_folder, parents=True)

    default_error_json = None
    if json_file_name == 'error':
        default_error_json = {
            'log_method': json_file_name.upper(),
            'log_message': log_message.split(' - ')[1].strip(),
            'log_reference_id': reference_id,
            'log_error': log_message.split(' - ')[1].split(' | ')[1],
            'log_stacktrace': log_message.split(' - ')[1].split(' | Error: ')[1].split(' | StackTrace: ')[1],
            'time_stamp': time_stamp
        }

    default_json = {
        'log_method': json_file_name.upper(),
        'log_message': log_message.split(' - ')[1].strip(),
        'log_reference_id': reference_id,
        'time_stamp': time_stamp
    }

    json_to_write = default_error_json if json_file_name == 'error' else default_json
    json_file = Path(json_file_folder / f'{json_file_name}.json')
    if json_file.exists() == False:
        json_file.write_text(data=json.dumps(obj=[json_to_write], indent=4), encoding='utf-8')
        return
    
    with json_file.open(mode='r', encoding='utf-8') as file:
        json_string = list(json.loads(file.read()))
        json_string.append(json_to_write)
        
        with json_file.open(mode="w", encoding="utf-8") as file:
            file.write(json.dumps(obj=json_string, indent=4))