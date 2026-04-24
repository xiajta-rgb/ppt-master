import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 读取生成的 WSGI
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_final.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

print(f"WSGI 长度: {len(wsgi_content)}")

# 上传 WSGI - 使用 multipart
boundary = uuid.uuid4().hex
headers = {
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

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
print("上传 WSGI...")
resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=30)
print(f"上传状态: {resp.status_code}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r.status_code}")
