import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 1. 检查当前 WSGI
print("检查 WSGI 内容...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
print(f"WSGI 状态: {r.status_code}")
if r.status_code == 200:
    print(f"WSGI 长度: {len(r.text)}")
    print("\nWSGI 内容:")
    print(r.text)

    # 检查关键配置
    if 'from urllib.parse import unquote' in r.text:
        print("\n[OK] WSGI 包含 unquote")
    else:
        print("\n[X] WSGI 缺少 unquote")

    if "PROJECT_DIR = '/home/ppt/ppt-master'" in r.text:
        print("[OK] PROJECT_DIR 正确")
    else:
        print("[X] PROJECT_DIR 可能不正确")

# 2. 测试 trace 端点
print("\n\n测试 /trace 端点...")
r = requests.get('https://ppt.pythonanywhere.com/trace', timeout=30)
print(f"trace 状态: {r.status_code}")
print(f"trace 内容:\n{r.text[:1000]}")
