import requests
import time

time.sleep(8)

# 测试 404 标记
r = requests.get('https://ppt.pythonanywhere.com/test123', timeout=30)
print(f"404: {r.status_code}")
if 'B64_V5' in r.text:
    print("[OK] B64_V5 WSGI 生效")
else:
    print("[X] B64_V5 WSGI 未生效")

# 测试首页
r2 = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"\n首页: {r2.status_code}, 长度: {len(r2.text)}")
if 'renderProjects()' in r2.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")
