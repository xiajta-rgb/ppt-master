import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

print("检查服务器上的 WSGI 配置...")

r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
if r.status_code == 200:
    print(f"\nWSGI 内容长度: {len(r.text)}")
    print("\n--- WSGI 内容 ---")
    print(r.text)
    print("--- WSGI 结束 ---")

    # 检查是否有 charset=utf-8
    if 'charset=utf-8' in r.text:
        print("\n[OK] WSGI 包含 charset=utf-8")
    else:
        print("\n[X] WSGI 缺少 charset=utf-8")

    # 检查 STATIC_DIR
    if 'PROJECT_DIR = ' in r.text:
        import re
        match = re.search(r"PROJECT_DIR = '([^']+)'", r.text)
        if match:
            print(f"\nPROJECT_DIR: {match.group(1)}")
else:
    print(f"无法获取 WSGI: {r.status_code}")
