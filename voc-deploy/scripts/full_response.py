import requests

# 测试 SVG 并查看完整响应
svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r = requests.get(svg_url, timeout=30)

print(f"状态: {r.status_code}")
print(f"完整响应:\n{r.text}")
