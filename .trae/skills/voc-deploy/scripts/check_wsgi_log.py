#!/usr/bin/env python3
"""
检查 PythonAnywhere WSGI 日志
"""

import requests
from urllib.parse import quote

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

# 读取 WSGI 日志文件
log_path = '/home/ppt/wsgi_export.log'
url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{log_path}'

try:
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        print("WSGI 日志内容:")
        print("=" * 60)
        # 显示最后 50 行
        lines = r.text.strip().split('\n')
        for line in lines[-50:]:
            print(line)
    else:
        print(f"[FAIL] Status: {r.status_code}")
        print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"[ERROR] {e}")
