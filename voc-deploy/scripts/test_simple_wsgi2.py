import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

SIMPLE_HTML = '''<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Hello World</h1>
<p>This is a test. RenderProjects check: RENDER_PROJECTS_HERE</p>
</body>
</html>'''

WSGI_CODE = f'''def application(environ, start_response):
    content = """{SIMPLE_HTML}"""
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]

'''

print(f"WSGI 长度: {len(WSGI_CODE)}")

headers = {'Authorization': f'Token {API_TOKEN}'}

print("删除 WSGI...")
r = requests.delete(f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}', headers=headers)
print(f"删除状态: {r.status_code}")

print("\n创建简单 WSGI...")
boundary = uuid.uuid4().hex

# 使用 files 参数
files = {
    'content': ('wsgi.py', WSGI_CODE, 'text/plain')
}

r2 = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}',
    headers={'Authorization': f'Token {API_TOKEN}'},
    files=files,
    timeout=30
)
print(f"创建状态: {r2.status_code}")
if r2.status_code != 201:
    print(f"响应: {r2.text}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r3 = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r3.status_code}")
