import requests

print("测试 P03 SVG...")
# P03_市场分析.svg 而不是 P03_行业分析.svg
svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P03_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90.svg'
r = requests.get(svg_url, timeout=30)
print(f"状态: {r.status_code}")

# 测试 P04
svg_url2 = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P04_%E4%BA%A7%E5%93%81%E8%AE%BE%E8%AE%A1DNA.svg'
r2 = requests.get(svg_url2, timeout=30)
print(f"P04 状态: {r2.status_code}")

# 检查 viewer.html 是否在列表中
r3 = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
if 'viewer.html' in r3.text:
    print("\n[OK] viewer.html 在首页引用中")
else:
    print("\n[X] viewer.html 不在首页引用中")
