import requests
import time

print("等待 30 秒...")
time.sleep(30)

print("检查日志文件...")
try:
    r = requests.get('https://ppt.pythonanywhere.com/wsgi_debug.log', timeout=30)
    print(f"日志状态: {r.status_code}")
    if r.status_code == 200:
        print(f"日志内容:\n{r.text}")
except Exception as e:
    print(f"获取日志失败: {e}")

print("\n测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    params={'project': 'demo_project_intro_ppt169_20251211'},
    timeout=180
)

print(f"\n导出状态: {r.status_code}")
if r.status_code == 500:
    print(f"错误: {r.text[:2000]}")
