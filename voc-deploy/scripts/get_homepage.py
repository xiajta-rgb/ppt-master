import requests

r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")

# 保存完整内容
with open('homepage.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print(f"已保存到 homepage.html，长度: {len(r.text)}")

# 查找 projects 数组
import re
projects_match = re.search(r'projects\s*=\s*\[(.*?)\];', r.text, re.DOTALL)
if projects_match:
    projects_content = projects_match.group(1)
    print(f"\nprojects 数组内容前 500 字符:\n{projects_content[:500]}")
else:
    print("\n未找到 projects 数组")

# 查找 renderProjects 函数
render_match = re.search(r'function renderProjects\(\)(.*?)\}', r.text, re.DOTALL)
if render_match:
    print(f"\nrenderProjects 函数前 300 字符:\n{render_match.group(0)[:300]}")
