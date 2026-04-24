import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_b64_v6.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

print(f"WSGI: {len(wsgi_content)} 字符")

files = {'content': ('wsgi.py', wsgi_content, 'text/plain')}

r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}',
    headers={'Authorization': f'Token {API_TOKEN}'},
    files=files,
    timeout=30
)
print(f"上传: {r.status_code}")

# Reload
r2 = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/',
    headers={'Authorization': f'Token {API_TOKEN}'},
    timeout=60
)
print(f"Reload: {r2.status_code}")
