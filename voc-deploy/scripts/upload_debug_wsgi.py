import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

WSGI_CONTENT = '''import os
import sys
from urllib.parse import unquote

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # 调试：记录原始路径和解码后的路径
    debug_info = f"ORIGINAL={repr(path)}"

    # URL 解码
    decoded_path = unquote(path, encoding='utf-8', errors='replace')
    debug_info += f",DECODED={repr(decoded_path)}"

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
        static_file = os.path.join(STATIC_DIR, decoded_path.lstrip('/'))
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
            content = '<html><body><h1>404: ' + decoded_path + '</h1><p>DEBUG:' + debug_info + '</p></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]

'''

boundary = uuid.uuid4().hex
headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
}

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="content"; filename="wsgi.py"\r\n'
    f'Content-Type: text/plain\r\n\r\n'
    f'{WSGI_CONTENT}\r\n'
    f'--{boundary}--\r\n'
)

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
print("上传调试 WSGI...")
resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=30)
print(f"上传状态: {resp.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"Reload 状态: {r.status_code}")
