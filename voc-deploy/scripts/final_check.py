import requests

print("测试网站当前状态...")

# 测试首页
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
print(f"首页长度: {len(r.text)}")

# 检查是否包含项目卡片 HTML
if 'project-card' in r.text:
    count = r.text.count('class="project-card"')
    print(f"[OK] 找到 {count} 个 project-card")
else:
    print("[X] 未找到 project-card")

# 检查关键项目
projects = ['心理治疗中的依恋', '亚马逊战术服装市场分析', '重庆市区域报告']
for p in projects:
    if p in r.text:
        print(f"[OK] 包含: {p}")
    else:
        print(f"[X] 缺少: {p}")

# 测试一个 SVG
print("\n测试 SVG 访问...")
svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r = requests.get(svg_url, timeout=30)
print(f"SVG 状态: {r.status_code}")

# 测试 viewer.html
print("\n测试 viewer.html...")
r = requests.get('https://ppt.pythonanywhere.com/viewer.html', timeout=30)
print(f"viewer.html 状态: {r.status_code}")

print("\n结论: 网站实际状态可能比测试结果更好，请用浏览器访问 https://ppt.pythonanywhere.com/ 确认")
