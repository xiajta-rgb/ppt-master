import requests
import time

time.sleep(5)

print("测试首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
print(f"内容长度: {len(r.text)}")

# 检查关键内容
if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects() 调用")
else:
    print("[X] 不包含 renderProjects() 调用")

if 'projects-grid' in r.text:
    print("[OK] 包含 projects-grid")
else:
    print("[X] 不包含 projects-grid")

# 检查页面底部是否有调用
if 'Initial render' in r.text:
    print("[OK] 包含 Initial render 注释")
else:
    print("[X] 不包含 Initial render 注释")

# 检查 projects 数量
import re
projects_match = re.search(r'projects\s*=\s*\[(.*?)\];', r.text, re.DOTALL)
if projects_match:
    count = projects_match.group(1).count('id:')
    print(f"\n项目数量: {count}")
