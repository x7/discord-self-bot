import sys
import os
import importlib.metadata
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
    
    print(f'Found {len(failed_libraries)} outdated module(s).')
    print(f'Found {len(uninstalled_libaries)} missing module(s).')
    for failed_library in failed_libraries:
        failed_name, failed_version, required_version = failed_library

        print(f'Library "{failed_name}" requires an update: {failed_version} → {required_version}')
        print(f'You can update it using: pip install --upgrade {failed_name}')

    for missing_library in uninstalled_libaries:
        print(f'Library "{missing_library}" needs to be installed you can install it by doing: pip install {missing_library}')

    valid_choies = ['y', 'n']
    while True:
        choice = input('⚠️ Some modules are outdated/missing.\n'
        'Would you like to automatically update/install these missing modules (y/n): ')

        if choice not in valid_choies:
            print("[!] Thats not a valid option, please choose again.")
            continue
        
        break

    success_install = []
    success_update = []
    if choice == 'y':
       # install modules
       for missing_library in uninstalled_libaries:
           install = install_library(missing_library)
           if install == True:
               success_install.append(missing_library)
               continue

       # update modules
       for failed_library in failed_libraries:
           update = update_library(failed_library)
           if update == True:
               success_update.append(failed_library)
               continue
           
    if len(success_install) == 0 and len(success_update) == 0:
        print(f'Failed to install/update any libraries. Please rerun this exiting program in 3 seconds...')
        time.sleep(3)

        return sys.exit()
    
    print(f'Successfully installed/updated {len(success_install) + len(success_update)}')
    print('Please restart the program to get the changes. This program will exit in 3 seconds...')
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
        print(f"Preflight library check failed: unable to locate {config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}. The program will exit in 3 seconds...")
        time.sleep(3)

        return sys.exit()
    
    try:
        requirements_content = requirements_file.read_text(encoding='utf-8').split('\n')
    except Exception as error:
        print(f'Preflight library check failed: unable to read {{config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}}. The program will exit in 3 seconds...')
        time.sleep(3)

        return sys.exit()
    
    if len(requirements_content) == 0:
        print(f'No libraries found in {config.RECOMMENDED_PYTHON_LIBRARY_VERSIONS_FILE}. The program will exit in 3 seconds...')
        time.sleep(3)

        return sys.exit()
    
    requirements_formatted = []
    for library in requirements_content:
        library_name, library_version = library.split('==')
        requirements_formatted.append([library_name.lower(), library_version])

    return requirements_formatted

def install_library(library_name):
    print(f'Starting installation of module "{library_name}"')
    install = os.system(f'python -m pip install {library_name}')

    if install == 0:
        print(f'Successfully completed installation of module "{library_name}"')
        return True
    
    if install == 1:
        print(f'Installation failed for "{library_name}" — module could not be located or is unavailable.Installation failed for "{library_name}" — module could not be located or is unavailable.')
        return False
    
    print(f'Install failed for "{library_name}" with exit code {install}')
    
    return False

def update_library(library_name):
    print(f'Beginning update for module {library_name}')
    update = os.system(f'python -m pip install --upgrade {library_name}')

    if update == 0:
        print(f'Successfully completed update of module "{library_name}"')
        return True

    if update == 1:
        print(f'Update failed for "{library_name}" — module could not be located or is unavailable.Installation failed for "{library_name}" — module could not be located or is unavailable.')
        return False
    
    print(f'Update failed for "{library_name}" with exit code {update}')
    
    return False