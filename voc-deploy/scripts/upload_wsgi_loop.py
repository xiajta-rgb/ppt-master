import requests
import time
import sys

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_with_export.py', 'r', encoding='utf-8') as f:
    wsgi_content = f.read()

print(f"WSGI 长度: {len(wsgi_content)}")

attempt = 0
while True:
    attempt += 1
    try:
        print(f"尝试 {attempt}: 上传 WSGI...")
        files = {'content': ('wsgi.py', wsgi_content, 'text/plain')}
        r = requests.post(
            f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}',
            headers={'Authorization': f'Token {API_TOKEN}'},
            files=files,
            timeout=60
        )
        print(f"上传状态: {r.status_code}")

        if r.status_code == 200:
            print("上传成功，Reload...")
            r2 = requests.post(
                f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/',
                headers={'Authorization': f'Token {API_TOKEN}'},
                timeout=60
            )
            print(f"Reload 状态: {r2.status_code}")
            print("完成!")
            break
        else:
            print(f"响应: {r.text[:200]}")

    except Exception as e:
        print(f"错误: {e}")

    time.sleep(3)
