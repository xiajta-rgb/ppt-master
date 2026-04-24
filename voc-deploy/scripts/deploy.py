#!/usr/bin/env python3
"""
PPT Master Deploy - 部署脚本
上传正确的 WSGI 文件并执行手动重载
"""

import requests
import sys
import argparse
from pathlib import Path

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
WEBAPP_DOMAIN = 'ppt.pythonanywhere.com'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

WSGI_CONTENT = '''import os
import sys

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = os.path.join(PROJECT_DIR)

sys.path.insert(0, PROJECT_DIR)

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    if path == '/' or path == '':
        index_file = os.path.join(STATIC_DIR, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            status = '200 OK'
            content_type = 'text/html'
        else:
            content = '<html><body><h1>index.html not found</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html'
    else:
        static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'r', encoding='utf-8') as f:
                content = f.read()
            status = '200 OK'
            if static_file.endswith('.html'):
                content_type = 'text/html'
            elif static_file.endswith('.css'):
                content_type = 'text/css'
            elif static_file.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'text/plain'
        else:
            content = f'<html><body><h1>404 Not Found: {path}</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html'

    response_headers = [('Content-Type', content_type), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)
    return [content.encode('utf-8')]
'''

def upload_wsgi():
    print("\n" + "="*50)
    print("Uploading WSGI file...")
    print("="*50)

    import uuid
    boundary = uuid.uuid4().hex
    headers = {
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    body = f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="wsgi.py"\r\nContent-Type: text/plain\r\n\r\n{WSGI_CONTENT}\r\n--{boundary}--\r\n'

    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
    try:
        resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=15)
        resp.raise_for_status()
        print("[OK] WSGI uploaded successfully")
        return True
    except Exception as e:
        print(f"[X] WSGI upload failed: {e}")
        return False

def verify():
    print("\n" + "="*50)
    print("Verifying website...")
    print("="*50)

    import time
    time.sleep(2)

    url = f"https://{WEBAPP_DOMAIN}/"
    try:
        response = requests.get(url, timeout=15)
        content_type = response.headers.get('Content-Type', '')
        text = response.text

        if response.status_code == 200 and 'text/html' in content_type and '<html' in text:
            print(f"[OK] Website is working!")
            print(f"     URL: {url}")
            print(f"     Status: {response.status_code}")
            return True
        else:
            print(f"[!] Website returned status {response.status_code}")
            print(f"     If you just deployed, please click Reload in PythonAnywhere web interface")
            return True
    except Exception as e:
        print(f"[!] Could not verify website: {e}")
        print(f"     Please check manually: https://{WEBAPP_DOMAIN}/")
        return True

def main():
    parser = argparse.ArgumentParser(description='PPT Master Deploy Script')
    args = parser.parse_args()

    print("="*50)
    print("PPT Master Deploy")
    print("="*50)
    print(f"Webapp: {WEBAPP_DOMAIN}")
    print(f"Project: /home/ppt/ppt-master")

    if not upload_wsgi():
        print("\n[X] Deployment failed: Could not upload WSGI")
        sys.exit(1)

    verify()

    print("\n" + "="*50)
    print("[OK] Deployment files uploaded!")
    print("="*50)
    print(f"\nIMPORTANT: Please manually reload the webapp:")
    print(f"1. Go to https://www.pythonanywhere.com/")
    print(f"2. Login and go to Web tab")
    print(f"3. Click Reload button for {WEBAPP_DOMAIN}")
    print(f"\nThen verify: https://{WEBAPP_DOMAIN}/")
    print("="*50)

if __name__ == '__main__':
    main()
