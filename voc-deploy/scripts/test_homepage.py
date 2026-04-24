import requests

print("测试主页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"主页状态: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type')}")
print(f"内容长度: {len(r.text)}")
print(f"前200字符: {r.text[:200]}")
