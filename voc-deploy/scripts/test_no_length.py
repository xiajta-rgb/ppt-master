import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

WSGI_CODE = f'''def application(environ, start_response):
    content = """{index_html}"""
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8')
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
print(f"上传: {r.status_code}")

r2 = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    timeout=60
)
print(f"Reload: {r2.status_code}")
