#!/usr/bin/env python3
"""
通过 PythonAnywhere API 直接执行 git pull
"""

import requests
import time

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

def run_command(cmd):
    result = requests.post(
        f'https://{HOST}/api/v0/user/{USERNAME}/consoles/',
        headers=HEADERS,
        json={'executable': '/bin/bash'},
        timeout=30
    )
    print(f"创建控制台: {result.status_code} {result.text[:200]}")
    
    if result.status_code in (200, 201):
        data = result.json()
        console_id = data.get('id')
        if not console_id:
            print(f"[!] 无 console_id: {data}")
            return False
        
        print(f"控制台 ID: {console_id}")
        
        exec_result = requests.post(
            f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/send_input/',
            headers=HEADERS,
            json={'input': cmd + '\n'},
            timeout=30
        )
        print(f"执行命令: {cmd}")
        print(f"执行结果: {exec_result.status_code}")
        
        time.sleep(15)
        
        requests.delete(
            f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}',
            headers=HEADERS,
            timeout=10
        )
        print("[OK] 命令已执行")
        return True
    return False

def check_file_content(path):
    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{path}'
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        content = r.text
        print(f"\n文件 {path} 内容 (前200字符):")
        print(content[:200])
        return content
    else:
        print(f"[FAIL] 读取 {path}: {r.status_code}")
        return None

# 先检查当前 viewer.html 的内容
print("=== 检查 PythonAnywhere 上的文件 ===")
content = check_file_content('/home/ppt/ppt-master/viewer.html')
if content and 'window.location.search' in content:
    print("[OK] viewer.html 已包含 URL 参数保留逻辑")
elif content and 'window.location.replace' in content:
    print("[FAIL] viewer.html 仍是旧版（不含 URL 参数保留）")

# 检查 public/viewer.html
content2 = check_file_content('/home/ppt/ppt-master/public/viewer.html')
if content2:
    print(f"public/viewer.html 长度: {len(content2)} 字符")

# 执行 git pull
print("\n=== 执行 git pull ===")
run_command('cd /home/ppt/ppt-master && git pull origin main')

# 等待后重新检查
time.sleep(5)
print("\n=== git pull 后检查 ===")
content3 = check_file_content('/home/ppt/ppt-master/viewer.html')
if content3 and 'window.location.search' in content3:
    print("[OK] git pull 后 viewer.html 已更新")
else:
    print("[FAIL] viewer.html 仍未更新，需要手动上传")
