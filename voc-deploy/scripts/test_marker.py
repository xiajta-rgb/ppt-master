import requests
import time

time.sleep(5)

print("测试标记 WSGI...")

# 测试一个 404 页面，看是否包含标记
r = requests.get('https://ppt.pythonanywhere.com/nonexistent12345', timeout=30)
print(f"测试页面状态: {r.status_code}")
print(f"响应内容: {r.text}")

if 'TEST_V3_20260424' in r.text:
    print("\n[OK] 标记存在 - WSGI 正在工作!")
else:
    print("\n[X] 标记不存在 - WSGI 没有执行新代码!")
