import requests
import time

# 添加时间戳绕过缓存
timestamp = int(time.time())
print(f"测试 with timestamp: {timestamp}")

url = f'https://ppt.pythonanywhere.com/?t={timestamp}'
r = requests.get(url, timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")
