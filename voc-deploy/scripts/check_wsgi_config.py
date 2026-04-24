import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查所有可能的 WSGI 文件
paths = [
    '/var/www/ppt_pythonanywhere_com_wsgi.py',
    '/var/www/ppt_pythonanywhere_com_wsgi.pyc',
    '/var/www/wsgi.py',
    '/var/www/wsgi_handlers.py',
]

for p in paths:
    r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{p}', headers=h)
    if r.status_code == 200:
        print(f"{p}: {len(r.text)} 字符")
    else:
        print(f"{p}: {r.status_code}")

# 检查 Web 应用配置
print("\n检查 Web 应用配置...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/webapps/', headers=h)
if r.status_code == 200:
    for app in r.json():
        print(f"Domain: {app.get('domain_name')}")
        print(f"Source: {app.get('source_directory')}")
        print(f"WSGI: {app.get('wsgi_config_file')}")
