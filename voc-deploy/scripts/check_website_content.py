import requests

url = "https://ppt.pythonanywhere.com/"

print("获取网站内容...")
r = requests.get(url, timeout=30)
print(f"状态码: {r.status_code}")

# 检查响应头
print(f"\n响应头 Content-Type: {r.headers.get('Content-Type')}")

# 检查返回内容
content = r.text
print(f"\n内容长度: {len(content)}")
print(f"是否包含 'const projects': {'const projects' in content}")

# 检查 projects 数组
import re
match = re.search(r'const projects = \[([\s\S]*?)\];', content)
if match:
    print(f"\n[OK] 找到 projects 数组")
    projects_str = match.group(1)
    count = projects_str.count('{')
    print(f"项目数量: {count}")
    titles = re.findall(r"title: '([^']+)'", projects_str)
    print(f"前3个项目: {titles[:3]}")
else:
    print(f"\n[问题] 未找到 projects 数组")

# 保存完整内容
with open(r'c:\Users\xmls\Documents\trae_projects\ppt-master\website_returned.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("\n已保存 website_returned.html")
