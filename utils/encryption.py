from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os
import traceback
from pathlib import Path
import config
import utils.log.logger as logger
import main

KEY_FULL_PATH = Path(Path.home() / "AppData" / "Roaming" / config.ENCRYPTION_FILE_LOCATION)

def encrypt_data(string):
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    encrypted = aesgcm.encrypt(nonce, string.encode(), None)
    combo = nonce + encrypted

    b64_key = base64.b64encode(key).decode()
    b64_encrypted = base64.b64encode(combo).decode()

    try:
        KEY_FULL_PATH.write_text(data=f'##### DONT SHARE THIS KEY #####\n{b64_key}', encoding='utf-8')
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message=f'Failed to write "{b64_key}" to key file',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )
    
    main.file_content_cache.add('encryption_key', b64_key)
    return b64_encrypted

def decrypt_data(encrypted_key):
    try:
        file_content_cache = main.file_content_cache.get('encryption_key')
        if file_content_cache == None:
            content = KEY_FULL_PATH.read_text(encoding='utf-8')
            secret_key = content.split('\n')[1].strip()
            main.file_content_cache.add('encryption_key', secret_key)
        else:
            secret_key = file_content_cache

        encrypted_data = base64.b64decode(encrypted_key)
        key = base64.b64decode(secret_key)
        nonce = encrypted_data[:12]

        ciphertext = encrypted_data[12:]
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)

        return decrypted.decode()
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message=f'Failed to decrypt "{encrypted_key}"',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )

        return None