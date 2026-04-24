import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 修复 URL 解码问题 - 添加 urllib.parse.unquote
FIXED_WSGI = '''import os
import sys
from urllib.parse import unquote

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

sys.path.insert(0, PROJECT_DIR)

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    path = unquote(path)

    if path == '/' or path == '':
        index_file = os.path.join(STATIC_DIR, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            status = '200 OK'
            content_type = 'text/html; charset=utf-8'
        else:
            content = '<html><body><h1>index.html not found</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'
    else:
        static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'r', encoding='utf-8') as f:
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
            else:
                content_type = 'text/plain; charset=utf-8'
        else:
            content = f'<html><body><h1>404 Not Found: {path}</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]

'''

def upload_wsgi():
    boundary = uuid.uuid4().hex
    headers = {
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    body = f'--{boundary}\\r\\nContent-Disposition: form-data; name="content"; filename="wsgi.py"\\r\\nContent-Type: text/plain\\r\\n\\r\\n{FIXED_WSGI}\\r\\n--{boundary}--\\r\\n'

    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
    resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=30)
    return resp.status_code in (200, 201)

print("上传修复后的 WSGI (添加 URL 解码)...")
if upload_wsgi():
    print("[OK] WSGI 已上传!")
    print("\\n请在 PythonAnywhere Web 界面点击 Reload")
else:
    print("[X] 上传失败")
