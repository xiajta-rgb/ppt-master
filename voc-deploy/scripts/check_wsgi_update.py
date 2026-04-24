import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查 WSGI 内容
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
print(f"WSGI 状态: {r.status_code}")
print(f"WSGI 长度: {len(r.text)}")
print(f"\nWSGI 内容:")
print(r.text)

# 检查是否包含 decode_path 函数
if 'def decode_path' in r.text:
    print("\n[OK] 包含 decode_path 函数")
else:
    print("\n[X] 缺少 decode_path 函数")

# 检查是否包含 unquote
if 'unquote' in r.text:
    print("[OK] 包含 unquote")
else:
    print("[X] 缺少 unquote")
