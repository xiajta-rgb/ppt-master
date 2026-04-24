import requests
import time

print("等待 10 秒...")
time.sleep(10)

print("测试网站首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
else:
    print("[X] 不包含 renderProjects()")

if 'Initial render' in r.text:
    print("[OK] 包含 Initial render")
else:
    print("[X] 不包含 Initial render")

print(f"\n最后 300 字符:\n{r.text[-300:]}")
