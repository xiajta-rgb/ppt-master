import requests

print("检查网站渲染的项目卡片...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)

# 检查是否生成了项目卡片 HTML
if 'project-card' in r.text:
    count = r.text.count('class="project-card"')
    print(f"[OK] 找到 {count} 个 project-card HTML 元素")
else:
    print("[X] 未找到 project-card，可能 JavaScript 没执行或 grid 为空")

# 检查 projects-grid 是否为空
import re
grid_match = re.search(r'<div class="projects-grid" id="projects-grid">([\s\S]*)</div>\s*</main>', r.text)
if grid_match:
    grid_content = grid_match.group(1).strip()
    if grid_content == '' or grid_content == '<!-- Projects will be inserted here by JavaScript -->':
        print("[X] projects-grid 为空 - JavaScript 可能没有执行")
    else:
        print(f"[OK] projects-grid 有内容，长度: {len(grid_content)}")
else:
    print("[!] 无法匹配 projects-grid")

# 检查是否缺少某个项目
print("\n检查是否包含关键项目...")
key_projects = ['亚马逊战术服装', '心理治疗中的依恋', '重庆市区域报告']
for p in key_projects:
    if p in r.text:
        print(f"  [OK] 包含: {p}")
    else:
        print(f"  [X] 缺少: {p}")

# 检查 renderProjects 调用
if 'renderProjects()' in r.text:
    print("\n[OK] renderProjects() 被调用")
else:
    print("\n[X] renderProjects() 未被调用")

# 截图关键 HTML 片段
print("\n--- index.html 中 projects-grid 附近内容 ---")
idx = r.text.find('projects-grid')
if idx != -1:
    print(r.text[idx:idx+500])
