import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 获取服务器 index.html
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=h)
print(f"API 状态: {r.status_code}")
print(f"API 长度: {len(r.text)}")

# 检查是否包含 renderProjects() 调用
if 'renderProjects()' in r.text:
    print("[OK] API 返回包含 renderProjects()")
else:
    print("[X] API 返回不包含 renderProjects()")

# 检查最后 200 字符
print(f"\nAPI 最后 200 字符:\n{r.text[-200:]}")

# 对比本地 index.html
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    local_content = f.read()

print(f"\n本地长度: {len(local_content)}")
if local_content == r.text:
    print("[OK] 内容完全一致")
else:
    print("[X] 内容不一致")
