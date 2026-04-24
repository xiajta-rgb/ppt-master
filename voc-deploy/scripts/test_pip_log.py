import requests
import time

print("等待 60 秒让 pip 安装...")
time.sleep(60)

print("检查日志文件...")
try:
    r = requests.get('https://ppt.pythonanywhere.com/pip_log.txt', timeout=30)
    print(f"日志状态: {r.status_code}")
    if r.status_code == 200:
        print(f"日志内容:\n{r.text}")
except Exception as e:
    print(f"获取日志失败: {e}")

print("\n测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    timeout=30
)

print(f"\n导出状态: {r.status_code}")
print(f"响应: {r.text[:500]}")
