import requests
import time

time.sleep(8)

# 测试 404 页面看标记
r = requests.get('https://ppt.pythonanywhere.com/nonexistent_test_12345', timeout=30)
print(f"测试页面状态: {r.status_code}")
print(f"响应:\n{r.text}")

if 'V3_20260424_171400' in r.text:
    print("\n[OK] 唯一标记存在 - 新 WSGI 生效!")
else:
    print("\n[X] 唯一标记不存在")
