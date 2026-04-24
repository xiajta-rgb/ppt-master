import requests
import time

time.sleep(8)

# 测试首页
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"首页: {r.status_code}, 长度: {len(r.text)}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")
    print(f"最后 200 字符:\n{r.text[-200:]}")

# 测试 404
r2 = requests.get('https://ppt.pythonanywhere.com/xyz', timeout=30)
if 'B64_V6' in r2.text:
    print("[OK] V6 WSGI 生效")
