import requests
import time

time.sleep(3)

print("测试 SVG 访问...")

# 测试中文 SVG
svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r = requests.get(svg_url, timeout=30)
print(f"SVG 状态: {r.status_code}")
if r.status_code == 200:
    print(f"[OK] SVG 可访问! 长度: {len(r.text)}")
else:
    print(f"[X] SVG 返回: {r.status_code}")
    print(f"响应: {r.text[:200]}")

# 测试首页
print("\n测试首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
if 'renderProjects()' in r.text:
    print("[OK] 首页包含 renderProjects()")
else:
    print("[X] 首页缺少 renderProjects()")
