import requests

# 尝试禁用压缩
headers = {
    'Accept-Encoding': 'identity',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

session = requests.Session()
session.headers.update(headers)

# 先清除可能存在的缓存
session.get('https://ppt.pythonanywhere.com/', timeout=30)

# 然后测试
r = session.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")
print(f"Content-Type: {r.headers.get('Content-Type')}")
print(f"Content-Length header: {r.headers.get('Content-Length')}")
print(f"Transfer-Encoding: {r.headers.get('Transfer-Encoding')}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
