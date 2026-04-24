import requests
import json

HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
API_TOKEN = 'your_api_token_here'

print("检查已安装的包...")
r = requests.get(
    f'https://{HOST}/api/v0/user/{USERNAME}/packages/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    timeout=30
)
print(f"状态: {r.status_code}")
if r.status_code == 200:
    packages = r.json()
    print(json.dumps(packages, indent=2)[:2000])
