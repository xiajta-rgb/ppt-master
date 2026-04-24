import requests
import json
import time

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

print("创建 Console ...")
r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/consoles/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    json={'executable': '/usr/bin/python3', 'arguments': '-m pip install python-pptx'},
    timeout=30
)
print(f"创建状态: {r.status_code}")
if r.status_code == 201:
    result = r.json()
    print(f"Console ID: {result.get('id')}")
    console_id = result.get('id')

    print("\n等待 10 秒让命令执行...")
    time.sleep(10)

    print("\n获取 Console 输出...")
    r2 = requests.get(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/',
        headers={'Authorization': f'Token {API_TOKEN}'},
        timeout=30
    )
    print(f"获取状态: {r2.status_code}")
    if r2.status_code == 200:
        print(f"输出: {r2.text[:2000]}")
else:
    print(f"响应: {r.text[:500]}")
