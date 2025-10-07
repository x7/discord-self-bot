import sys
import importlib.metadata
import colorama
from pathlib import Path
import time
import traceback
import config
import utils.log.logger as logger

def check_libraries():
    required_libraries = get_required_libraries()
    installed_libraries = get_installed_libraries(required_libraries=required_libraries)

    failed_libraries = []
    uninstalled_libaries = []
    for required_library in required_libraries:
        name = required_library[0]
        version = tuple(map(int, required_library[1].replace('.', '')))
        found_library = False

        for installed_library in installed_libraries:
            installed_name = installed_library[0]
            if name != installed_name:
                continue

            # found it compare versions
            installed_version = tuple(map(int, installed_library[1].replace('.', '')))
            if version >= installed_version:
                found_library = True
                continue

            # module name | installed version | required version
            failed_libraries.append([installed_name, installed_library[1], required_library[1]])
            found_library = True

        if found_library == False:
            uninstalled_libaries.append(name)

    if len(failed_libraries) == 0 and len(uninstalled_libaries) == 0:
        logger.logger(log_method='info', log_message='Library preflight check completed — no outdated or missing modules found.')
        return
    
    logger.logger(log_method='warn', log_message=f'Found {len(failed_libraries)} outdated module(s).')
    logger.logger(log_method='warn', log_message=f'Found {len(uninstalled_libaries)} missing module(s).')
    for failed_library in failed_libraries:
        failed_name, failed_version, required_version = failed_library

        logger.logger(
            log_method='warn',
            log_message=f'Library "{failed_name}" requires an update: {failed_version} → {required_version}'
        )
        logger.logger(
            log_method='info',
            log_message=f'You can update it using: pip install --upgrade {failed_name}'
        )

    for missing_library in uninstalled_libaries:
        logger.logger(
            log_method='info',
            log_message=f'Library "{missing_library}" needs to be installed you can install it by doing: pip install {missing_library}'
        )

    valid_choies = ['y', 'n']
    while True:
        choice = input(colorama.Fore.CYAN + '⚠️ Some modules are outdated/missing.\n'
        'It is recommended that you exit the program and install/update them before continuing.\n'
        'Do you want to exit now? (y/n): ')

        if choice not in valid_choies:
            print(colorama.Fore.RED + "[!] Thats not a valid option, please choose again.")
            continue
        
        break

    if choice == 'y':
        logger.logger(log_method='info', log_message='Exiting program in 3 seconds...')
        time.sleep(3)

        return sys.exit()

def get_installed_libraries(required_libraries):
    libraries = []

    for library in importlib.metadata.distributions():
        library_name = library.metadata['name'].lower()
        library_version = library.version
        
        if any(package[0].lower() == library_name for package in required_libraries):
            libraries.append([library_name, library_version]) 

    return libraries

def get_required_libraries():
    requirements_file = Path(Path.cwd() / config.RECOMMENDED_PYTHON_LIBRARY_VERISONS_FILE)
    
    if requirements_file.exists() == False:
        logger.logger(log_error='error', log_message=f"Preflight library check failed: unable to locate {config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}. The program will exit in 3 seconds...")
        time.sleep(3)

        return sys.exit()
    
    try:
        requirements_content = requirements_file.read_text(encoding='utf-8').split('\n')
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message=f'Preflight library check failed: unable to read {{config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}}. The program will exit in 3 seconds...',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )
        time.sleep(3)

        return sys.exit()
    
    if len(requirements_content) == 0:
        logger.logger(log_method='error', log_message=f'No libraries found in {config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}. The program will exit in 3 seconds...')
        time.sleep(3)

        return sys.exit()
    
    requirements_formatted = []
    for library in requirements_content:
        library_name, library_version = library.split('==')
        requirements_formatted.append([library_name.lower(), library_version])

    return requirements_formatted