import requests
from urllib.parse import urlparse, unquote

# 检查 requests 发送的 URL
url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'

print(f"原始 URL: {url}")
print(f"URL 是否包含 %: {'%' in url}")

# 解析 URL
parsed = urlparse(url)
print(f"path 部分: {parsed.path}")

# unquote 后
decoded = unquote(parsed.path, encoding='utf-8')
print(f"unquote 后: {decoded}")

# 测试直接用解码后的 URL
print("\n测试解码后的 URL...")
r = requests.get(f'https://ppt.pythonanywhere.com{decoded}', timeout=30)
print(f"状态: {r.status_code}")
print(f"响应: {r.text[:200] if r.status_code != 200 else 'OK'}")
