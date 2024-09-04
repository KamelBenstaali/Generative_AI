import requests

# Replace these with your actual credentials
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REFRESH_TOKEN = 'your-refresh-token'

# Function to get OAuth 2.0 token
def get_oauth_token(client_id, client_secret, refresh_token):
    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    response = requests.post(token_url, data=payload)
    token_info = response.json()
    return token_info['access_token']

# Obtain OAuth 2.0 token
access_token = get_oauth_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

# Make an authenticated request to the protected resource
headers = {
    'Authorization': f'Bearer {access_token}'
}

# URL of the protected resource
protected_url = 'https://api.your-private-website.com/protected-resource'

response = requests.get(protected_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful!")
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
