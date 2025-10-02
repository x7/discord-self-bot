import requests

# TODO: Handle in try catch
def get_discord_user_data(token):
    request_headers = {
        'Authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

    request = requests.get('https://discord.com/api/v9/users/@me', headers=request_headers)
    data = request.json()

    if request.status_code != 200:
        return { 'success': False, 'error_message': data['message'], 'error_code': data['code']}
    
    return { 'success': True, 'data': data }