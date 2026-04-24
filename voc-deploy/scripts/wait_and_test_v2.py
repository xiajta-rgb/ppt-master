import requests
import time

print("等待 5 秒后测试...")
time.sleep(5)

print("\n测试首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页状态: {r.status_code}")
if r.status_code == 200:
    if '亚马逊战术服装' in r.text:
        print("[OK] 首页内容正确")
    else:
        print("[X] 首页内容异常")

print("\n测试 ASCII SVG...")
r = requests.get('https://ppt.pythonanywhere.com/examples/TacticalClothingReport/svg_final/slide_01_cover.svg', timeout=30)
print(f"ASCII SVG 状态: {r.status_code}")

print("\n测试中文 SVG (URL 编码)...")
r = requests.get('https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg', timeout=30)
print(f"中文 SVG 状态: {r.status_code}")

if r.status_code == 200:
    print("[OK] 问题已修复!")
else:
    print("[X] 还需要 reload 或有其他问题")
