import requests
import time

time.sleep(8)

# 测试 404 标记
r = requests.get('https://ppt.pythonanywhere.com/nonexistent', timeout=30)
print(f"404 测试: {r.status_code}")
if 'B64_V4' in r.text:
    print("[OK] 新 WSGI 生效")
else:
    print("[X] 新 WSGI 未生效")

# 测试首页
print("\n测试首页...")
r2 = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r2.status_code}")
print(f"长度: {len(r2.text)}")

if 'renderProjects()' in r2.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")

if 'Initial render' in r2.text:
    print("[OK] 包含 Initial render")
