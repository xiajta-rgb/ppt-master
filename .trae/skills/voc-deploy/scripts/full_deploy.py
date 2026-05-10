#!/usr/bin/env python3
"""
通过 PythonAnywhere Schedule API 执行 git pull
"""

import requests
import time

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

# 使用系统命令执行 git pull
# PythonAnywhere 的 Schedule API 可以创建计划任务
# 但更简单的方式是直接通过 Files API 检查和上传

def check_file(path):
    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{path}'
    r = requests.get(url, headers=HEADERS, timeout=10)
    return r.status_code, r.text if r.status_code == 200 else ''

# 检查关键文件
print("=== 检查 PythonAnywhere 上的关键文件 ===")

files_to_check = [
    '/home/ppt/ppt-master/viewer.html',
    '/home/ppt/ppt-master/public/viewer.html',
    '/home/ppt/ppt-master/public/viewer.js',
    '/home/ppt/ppt-master/public/js/collections.js',
]

for f in files_to_check:
    status, content = check_file(f)
    if status == 200:
        has_search = 'window.location.search' in content
        has_replace = 'window.location.replace' in content
        print(f"[OK] {f} ({len(content)} chars) search={has_search} replace={has_replace}")
    else:
        print(f"[MISSING] {f} - status {status}")

# 直接上传 viewer.html 到根目录
print("\n=== 上传 viewer.html 到根目录 ===")

viewer_redirect = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting to Viewer...</title>
    <script>
        var target = 'public/viewer.html' + window.location.search + window.location.hash;
        window.location.replace(target);
    </script>
</head>
<body>
    <p>Redirecting to <a href="public/viewer.html">Slide Gallery Viewer</a>...</p>
</body>
</html>'''

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path/home/ppt/ppt-master/viewer.html'
r = requests.post(url, headers=HEADERS, files={'content': viewer_redirect}, timeout=30)
print(f"上传 viewer.html: {r.status_code}")

# 重载 Web App
print("\n=== 重载 Web App ===")
url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/{WEBAPP_DOMAIN}/reload/'
r = requests.post(url, headers=HEADERS, timeout=90)
print(f"重载: {r.status_code}")

time.sleep(5)

# 验证
print("\n=== 验证 ===")
test_urls = [
    ("首页", "https://ppt.pythonanywhere.com/"),
    ("Viewer", "https://ppt.pythonanywhere.com/viewer.html"),
    ("API", "https://ppt.pythonanywhere.com/api/scan-projects"),
    ("Check", "https://ppt.pythonanywhere.com/api/check-changes"),
    ("SVG", "https://ppt.pythonanywhere.com/examples/ppt169_%E9%A1%B6%E7%BA%A7%E5%92%A8%E8%AF%A2%E9%A3%8E_%E9%87%8D%E5%BA%86%E5%B8%82%E5%8C%BA%E5%9F%9F%E6%8A%A5%E5%91%8A_ppt169_20251213/svg_final/P01_%E5%B0%81%E9%9D%A2.svg"),
]

for name, url in test_urls:
    try:
        r = requests.get(url, timeout=15)
        print(f"[{'OK' if r.status_code == 200 else 'FAIL'}] {name}: {r.status_code} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
