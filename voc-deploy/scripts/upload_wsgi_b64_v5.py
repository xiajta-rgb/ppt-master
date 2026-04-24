import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_b64_v5.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

print(f"WSGI 长度: {len(wsgi_content)}")

# 使用 files 参数上传
files = {
    'content': ('wsgi.py', wsgi_content, 'text/plain')
}

r = requests.post(
    f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}',
    headers={'Authorization': f'Token {API_TOKEN}'},
    files=files,
    timeout=30
)
print(f"上传状态: {r.status_code}")
if r.status_code != 201:
    print(f"响应: {r.text[:500]}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r2 = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r2.status_code}")
