import requests

# 测试纯 ASCII 路径是否正常
print("测试 ASCII 路径是否正常...")

# TacticalClothingReport 是 ASCII 名称
url = 'https://ppt.pythonanywhere.com/examples/TacticalClothingReport/svg_final/slide_01_cover.svg'
r = requests.get(url, timeout=30)
print(f"ASCII 路径状态: {r.status_code}")
if r.status_code == 200:
    print("[OK] ASCII 路径正常，WSGI 没有被破坏")
else:
    print(f"[X] ASCII 路径也失败了")

# 测试带中文的 TacticalClothingReport 中的中文 SVG 名称
url2 = 'https://ppt.pythonanywhere.com/examples/TacticalClothingReport/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r2 = requests.get(url2, timeout=30)
print(f"\nTacticalClothingReport 中编码的中文 SVG: {r2.status_code}")

print("\n注意: 需要 Reload 才能让新的 WSGI 生效!")
