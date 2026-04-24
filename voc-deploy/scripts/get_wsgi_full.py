import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
print(f"WSGI 长度: {len(r.text)}")
print("\n完整 WSGI 内容:")
print(r.text)
