import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=h)

# 查找 INDEX_CONTENT
import re
match = re.search(r'INDEX_CONTENT = """(.{0,500})..."""', r.text, re.DOTALL)
if match:
    content = match.group(1)[:500]
    print(f"INDEX_CONTENT 开头:\n{content}")
else:
    print("未找到 INDEX_CONTENT")

# 检查整个 WSGI 长度
print(f"\nWSGI 总长度: {len(r.text)}")
