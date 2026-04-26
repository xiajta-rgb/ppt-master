#!/usr/bin/env python3
"""
PPT Master Deploy - 统一部署脚本
上传正确的 WSGI 并重载 Web 应用
"""

import subprocess
import time
import requests
import sys
from pathlib import Path

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
WEBAPP_DOMAIN = 'ppt.pythonanywhere.com'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent

WSGI_CONTENT = '''import os
import sys
import urllib.parse

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

LOG_FILE = '/home/ppt/wsgi_export.log'

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            import datetime
            f.write(datetime.datetime.now().isoformat() + ' ' + msg + '\\n')
            f.flush()
    except:
        pass

log('WSGI starting')

def read_index_html():
    INDEX_FILE = os.path.join(STATIC_DIR, 'public', 'index.html')
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    INDEX_FILE = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return '<html><body><h1>index.html not found</h1></body></html>'

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    log('request: ' + path)

    if path == '/' or path == '':
        content = read_index_html()
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
    else:
        static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'rb') as f:
                content = f.read()
            status = '200 OK'
            if static_file.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif static_file.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif static_file.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            elif static_file.endswith('.svg'):
                content_type = 'image/svg+xml; charset=utf-8'
            elif static_file.endswith('.png'):
                content_type = 'image/png'
            elif static_file.endswith('.jpg') or static_file.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'text/plain; charset=utf-8'
        else:
            content = ('<html><body><h1>404: ' + path + '</h1></body></html>').encode('utf-8')
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [('Content-Type', content_type)]
    start_response(status, response_headers)

    if isinstance(content, str):
        return [content.encode('utf-8')]
    return [content]
'''

def upload_wsgi():
    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
    try:
        resp = requests.post(url, headers=HEADERS, files={'content': WSGI_CONTENT}, timeout=30)
        resp.raise_for_status()
        print("[OK] WSGI 上传成功")
        return True
    except Exception as e:
        print(f"[X] WSGI 上传失败: {e}")
        return False

def reload_webapp():
    url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/{WEBAPP_DOMAIN}/reload/'
    try:
        resp = requests.post(url, headers=HEADERS, timeout=90)
        resp.raise_for_status()
        print("[OK] Web App 重载成功!")
        return True
    except Exception as e:
        print(f"[X] Web App 重载失败: {e}")
        return False

def verify():
    print("\n" + "="*50)
    print("验证网站...")
    print("="*50)

    url = "https://ppt.pythonanywhere.com/"
    max_retries = 3
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200 and len(response.text) > 1000:
                print(f"[OK] 网站验证成功!")
                print(f"     URL: {url}")
                print(f"     Status: {response.status_code}")
                print(f"     Content-Length: {len(response.text)}")
                return True
            else:
                print(f"[X] 验证失败 (尝试 {attempt+1}/{max_retries})")
        except Exception as e:
            print(f"[X] 请求失败 (尝试 {attempt+1}/{max_retries}): {e}")

        if attempt < max_retries - 1:
            print(f"[INFO] {retry_delay}秒后重试...")
            time.sleep(retry_delay)

    print("[X] 验证失败")
    return False

def main():
    print("\n" + "#"*50)
    print("# PPT Master Deploy - 部署脚本")
    print("#"*50)

    print("\n[Step 1] 上传 WSGI...")
    if not upload_wsgi():
        print("\n[X] WSGI 上传失败")
        sys.exit(1)

    print("\n[Step 2] 重载 Web App...")
    if not reload_webapp():
        print("\n[!] 重载失败，请手动重载")
    else:
        time.sleep(3)

    print("\n[Step 3] 验证网站...")
    verify()

    print("\n" + "#"*50)
    print("# 部署完成!")
    print("#"*50)
    print(f"\n访问: https://ppt.pythonanywhere.com/")

if __name__ == "__main__":
    main()