import requests
import utils.log.logger as logger
import traceback

def get_discord_user_data(token):
    request_headers = {
        'Authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

    try:
        request = requests.get('https://discord.com/api/v9/users/@me', headers=request_headers, timeout=10)
        data = request.json()
    except Exception as error:
        logger.logger(
            log_method='error',
            log_message='Unable to retrieve Discord user data',
            log_error=error,
            log_stacktrace=traceback.format_exc()
        )

        return { 'success': False, 'error_message': f'Discord API request failed (HTTP {request.status_code})' }

    if request.status_code != 200:
        return { 'success': False, 'error_message': data['message'] }
    
    return { 'success': True, 'data': data }