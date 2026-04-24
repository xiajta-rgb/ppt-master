import requests
import time

time.sleep(3)

print("全面测试...")

# 测试多个 SVG
svg_tests = [
    '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg',
    '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P02_%E7%9B%AE%E5%BD%95.svg',
    '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P03_%E8%A1%8C%E4%B8%9A%E5%88%86%E6%9E%90.svg',
]

for svg in svg_tests:
    url = f'https://ppt.pythonanywhere.com{svg}'
    r = requests.get(url, timeout=30)
    status = "✓" if r.status_code == 200 else "✗"
    print(f"{status} {svg.split('/')[-2]}/{svg.split('/')[-1]} - {r.status_code}")

# 测试 viewer.html
print("\n测试 viewer.html...")
r = requests.get('https://ppt.pythonanywhere.com/viewer.html', timeout=30)
print(f"viewer.html 状态: {r.status_code}")

# 测试首页
print("\n测试首页渲染...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
print(f"包含 renderProjects: {'renderProjects' in r.text}")
print(f"包含 examples: {'examples' in r.text}")
