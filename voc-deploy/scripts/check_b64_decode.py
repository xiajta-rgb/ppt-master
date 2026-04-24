import base64
import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=h)

# 查找 INDEX_B64
idx = r.text.find('INDEX_B64 = """')
if idx == -1:
    print("未找到 INDEX_B64")
    exit()

# 找结束位置
end = r.text.find('"""', idx + 15)
b64 = r.text[idx + 15:end]

print(f"Base64 长度: {len(b64)}")

# 检查 base64 是否有换行符
if '\n' in b64 or '\r' in b64:
    print("[X] Base64 包含换行符!")
else:
    print("[OK] Base64 无换行符")

# 尝试解码
try:
    decoded = base64.b64decode(b64).decode('utf-8')
    print(f"解码后长度: {len(decoded)}")
    if 'renderProjects()' in decoded:
        print("[OK] 解码内容包含 renderProjects()")
    else:
        print("[X] 解码内容不包含 renderProjects()")
except Exception as e:
    print(f"解码错误: {e}")
