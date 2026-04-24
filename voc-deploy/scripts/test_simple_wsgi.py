import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 最简单的 WSGI - 纯 ASCII
SIMPLE_HTML = '''<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Hello World</h1>
<p>This is a test. RenderProjects check: RENDER_PROJECTS_HERE</p>
<p>Chars: 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz</p>
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
headers2 = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
}

body = (
    f'--{boundary}\\r\\n'
    f'Content-Disposition: form-data; name="content"; filename="wsgi.py"\\r\\n'
    f'Content-Type: text/plain\\r\\n\\r\\n'
    f'{WSGI_CODE}\\r\\n'
    f'--{boundary}--\\r\\n'
)

r2 = requests.post(f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}', headers=headers2, data=body.encode('utf-8'), timeout=30)
print(f"创建状态: {r2.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r3 = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"Reload 状态: {r3.status_code}")
