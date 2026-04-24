import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

headers = {'Authorization': f'Token {API_TOKEN}'}

# 删除 WSGI
print("删除 WSGI...")
r = requests.delete(f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}', headers=headers)
print(f"删除状态: {r.status_code}")

# 读取 WSGI 内容
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_final.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

# 重新创建
print("\n重新创建 WSGI...")
import uuid
boundary = uuid.uuid4().hex
headers2 = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
}

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="content"; filename="wsgi.py"\r\n'
    f'Content-Type: text/plain\r\n\r\n'
    f'{wsgi_content}\r\n'
    f'--{boundary}--\r\n'
)

r2 = requests.post(f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}', headers=headers2, data=body.encode('utf-8'), timeout=30)
print(f"创建状态: {r2.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r3 = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r3.status_code}")
print(f"Reload 响应: {r3.text}")
