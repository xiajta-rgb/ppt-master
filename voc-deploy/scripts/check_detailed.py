import requests

print("详细检查请求...")

# 测试首页
session = requests.Session()
r = session.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
print(f"内容长度: {len(r.text)}")
print(f"Content-Type: {r.headers.get('Content-Type')}")
print(f"编码: {r.encoding}")

# 测试 SVG
r2 = session.get('https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg', timeout=30)
print(f"\nSVG 状态: {r2.status_code}")
print(f"SVG Content-Type: {r2.headers.get('Content-Type')}")
