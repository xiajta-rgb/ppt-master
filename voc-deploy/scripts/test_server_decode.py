import requests
import json

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
USERNAME = 'ppt'

# 创建 Console
url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/consoles/'
headers = {'Authorization': f'Token {API_TOKEN}'}

print("创建 Console...")
r = requests.post(url, headers=headers, json={}, timeout=30)
print(f"创建状态: {r.status_code}")

if r.status_code == 201:
    data = r.json()
    console_id = data.get('id')
    print(f"Console ID: {console_id}")

    # 发送命令
    cmd_url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/consoles/{console_id}/send_input/'
    code = 'from urllib.parse import unquote; path = "/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg"; print(unquote(path, encoding="utf-8"))'
    r2 = requests.post(cmd_url, headers=headers, json={'text': code + '\n'}, timeout=30)
    print(f"命令状态: {r2.status_code}")

    # 获取输出
    import time
    time.sleep(2)
    output_url = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/consoles/{console_id}/get_output/'
    r3 = requests.get(output_url, headers=headers, timeout=30)
    print(f"输出状态: {r3.status_code}")
    print(f"输出: {r3.text}")
else:
    print(f"响应: {r.text}")
