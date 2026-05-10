#!/usr/bin/env python3
"""
检查 WSGI 日志和当前状态
"""

import requests
import time

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
WEBAPP_DOMAIN = 'ppt.pythonanywhere.com'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

# 先重载 Web App
print("重载 Web App...")
url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/{WEBAPP_DOMAIN}/reload/'
r = requests.post(url, headers=HEADERS, timeout=90)
print(f"重载: {r.status_code}")

time.sleep(8)

# 检查网站是否恢复
print("\n检查网站...")
r = requests.get("https://ppt.pythonanywhere.com/", timeout=15)
print(f"首页: {r.status_code}")

# 读取 WSGI 日志
print("\n读取 WSGI 日志...")
url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path/home/ppt/wsgi_export.log'
r = requests.get(url, headers=HEADERS, timeout=10)
if r.status_code == 200:
    lines = r.text.strip().split('\n')
    print(f"日志行数: {len(lines)}")
    for line in lines[-30:]:
        print(f"  {line}")
else:
    print(f"无法读取日志: {r.status_code}")

# 检查错误日志
print("\n读取服务器错误日志...")
for log_path in ['/home/ppt/logs/user.error.log', '/var/log/user.error.log']:
    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{log_path}'
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        lines = r.text.strip().split('\n')
        print(f"{log_path}: {len(lines)} lines")
        for line in lines[-20:]:
            print(f"  {line[:200]}")
    else:
        print(f"{log_path}: {r.status_code}")
