import requests
import time

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
USERNAME = 'ppt'

print("安装 python-pptx...")

r = requests.post(
    f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/bash/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    json={'command': 'pip install --user python-pptx'},
    timeout=120
)
print(f"状态: {r.status_code}")
print(f"响应: {r.text[:1000]}")
