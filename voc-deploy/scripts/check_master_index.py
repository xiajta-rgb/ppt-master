import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查 index.html 是否存在
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=h)
print(f"index.html 状态: {r.status_code}")
print(f"index.html 长度: {len(r.text)}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")

# 检查最后 200 字符
print(f"\n最后 200 字符:\n{r.text[-200:]}")
