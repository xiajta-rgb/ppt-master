import requests

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 读取生成的 WSGI
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_final.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

print(f"WSGI 长度: {len(wsgi_content)}")

# 上传 WSGI
headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': 'text/plain'
}

url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
print("上传 WSGI...")
resp = requests.post(url, headers=headers, data=wsgi_content.encode('utf-8'), timeout=30)
print(f"上传状态: {resp.status_code}")
print(f"响应: {resp.text[:200] if resp.text else 'empty'}")

# Reload
reload_url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
r = requests.post(reload_url, headers={'Authorization': f'Token {API_TOKEN}'}, timeout=60)
print(f"\nReload 状态: {r.status_code}")
print(f"Reload 响应: {r.text}")
