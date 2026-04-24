import requests

# 测试 SVG 并查看调试信息
svg_path = 'examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
url = f'https://ppt.pythonanywhere.com/{svg_path}'

print(f"测试 URL: {url}")
r = requests.get(url, timeout=30)
print(f"状态: {r.status_code}")

# 查看响应内容（可能是调试信息）
print(f"\n响应内容:\n{r.text[:500]}")

# 解码后的路径测试
from urllib.parse import unquote
decoded_path = unquote(svg_path)
print(f"\n解码后路径: {decoded_path}")

# 直接用解码后的路径测试
url2 = f'https://ppt.pythonanywhere.com/{decoded_path}'
print(f"\n解码后 URL: {url2}")
r2 = requests.get(url2, timeout=30)
print(f"状态: {r2.status_code}")
print(f"响应: {r2.text[:500]}")
