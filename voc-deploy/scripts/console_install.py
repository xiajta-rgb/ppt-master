import requests
import json
import time

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

print("创建 Console 安装 python-pptx...")
r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/consoles/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    json={
        'executable': '/usr/bin/python3',
        'arguments': '-m pip install python-pptx --user'
    },
    timeout=30
)
print(f"创建状态: {r.status_code}")
if r.status_code == 201:
    result = r.json()
    console_id = result.get('id')
    print(f"Console ID: {console_id}")

    print("\n等待 15 秒让命令执行...")
    time.sleep(15)

    print("\n获取 Console 输出...")
    r2 = requests.get(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/',
        headers={'Authorization': f'Token {API_TOKEN}'},
        timeout=30
    )
    print(f"获取状态: {r2.status_code}")
    if r2.status_code == 200:
        output = r2.json()
        print(f"输出: {json.dumps(output, indent=2)[:3000]}")
else:
    print(f"响应: {r.text[:500]}")

print("\n" + "="*50)
print("再次创建 Console 验证安装...")
r3 = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/consoles/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    json={
        'executable': '/usr/bin/python3',
        'arguments': '-c "import pptx; print(pptx.__version__)"'
    },
    timeout=30
)
print(f"创建状态: {r3.status_code}")
if r3.status_code == 201:
    result = r3.json()
    console_id = result.get('id')
    print(f"Console ID: {console_id}")

    time.sleep(10)

    r4 = requests.get(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/',
        headers={'Authorization': f'Token {API_TOKEN}'},
        timeout=30
    )
    print(f"获取状态: {r4.status_code}")
    if r4.status_code == 200:
        output = r4.json()
        print(f"验证输出: {json.dumps(output, indent=2)[:3000]}")
