import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

SIMPLE_HTML = '''<!DOCTYPE html>
<html>
<head><title>Test Chinese</title></head>
<body>
<h1>测试中文 Chinese</h1>
<p>项目列表: RENDER_PROJECTS_HERE</p>
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

files = {'content': ('wsgi.py', WSGI_CODE, 'text/plain')}

r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}',
    headers={'Authorization': f'Token {API_TOKEN}'},
    files=files,
    timeout=30
)
print(f"上传状态: {r.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r2 = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"Reload 状态: {r2.status_code}")
