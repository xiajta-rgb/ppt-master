import requests
import time

time.sleep(5)

print("测试 SVG 访问...")

svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r = requests.get(svg_url, timeout=30)
print(f"中文 SVG 状态: {r.status_code}")
if r.status_code == 200:
    print(f"[OK] SVG 可访问! 长度: {len(r.text)}")
else:
    print(f"响应: {r.text[:300]}")

# 测试另一个
svg_url2 = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P02_%E7%9B%AE%E5%BD%95.svg'
r2 = requests.get(svg_url2, timeout=30)
print(f"\n第二个 SVG 状态: {r2.status_code}")
