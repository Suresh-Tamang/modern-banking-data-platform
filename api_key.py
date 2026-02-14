import requests
import os
from dotenv import load_dotenv, set_key

# Use 'json' to send data in the body, not the URL
payload = {
    'username': 'admin',
    'password': 'admin'
}
env_path = '.env'
response = requests.post(
    'http://127.0.0.1:9000/api/token/create/',
    json=payload
)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("API Key Retrieved Successfully")
    # Using .get() is smart—it prevents a KeyError if 'api_key' is missing
    api_key = response.json().get('access')
    if not os.path.exists(env_path):
        open(env_path,"a").close()
    set_key(env_path,'API_KEY',api_key)
    print(f"API Key: {api_key}")
    # Save the API key to the .env file
    set_key(env_path, 'API_KEY', api_key)
else:
    print("Failed to retrieve API Key")
    print(f"Error Detail: {response.text}")
