import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'

# 读取本地 index.html
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

print(f"index.html 长度: {len(index_content)}")

# 上传到服务器
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 创建新的 WSGI，只提供 index.html
WSGI_CONTENT = '''import os
import sys

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # WSGI 使用 Latin-1 编码路径，URL 编码的 UTF-8 字节被错误解释
    # 正确方法：用 Latin-1 编码回字节，然后用 UTF-8 解码
    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

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
            content = '<html><body><h1>404: ' + path + '</h1></body></html>'
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
print("上传 WSGI...")
resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=30)
print(f"上传状态: {resp.status_code}")

# 上传 index.html 到服务器
index_file_path = '/home/ppt/ppt-master/index.html'
boundary2 = uuid.uuid4().hex
headers2 = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary2}'
}
body2 = (
    f'--{boundary2}\r\n'
    f'Content-Disposition: form-data; name="content"; filename="index.html"\r\n'
    f'Content-Type: text/html\r\n\r\n'
    f'{index_content}\r\n'
    f'--{boundary2}--\r\n'
)

url2 = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{index_file_path}'
print("\n上传 index.html...")
resp2 = requests.post(url2, headers=headers2, data=body2.encode('utf-8'), timeout=30)
print(f"上传状态: {resp2.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r.status_code}")
print(f"Reload 响应: {r.text}")
