import requests
import base64

client_id = '1ed00775cb1d41a4800f19860059df5f'
client_secret = 'f4d78ba2fd044b27a4b75961c5534005'
redirect_uri = 'http://localhost:8888/callback'
code = 'AUTHORIZATION_CODE_RECEIVED'

# Encode client credentials
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = 'https://accounts.spotify.com/api/token'

token_data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
}

token_headers = {
    'Authorization': f'Basic {client_creds_b64.decode()}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

r = requests.post(token_url, data=token_data, headers=token_headers)
token_response_data = r.json()

access_token = token_response_data['access_token']
refresh_token = token_response_data['refresh_token']
