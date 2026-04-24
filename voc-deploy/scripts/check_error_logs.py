import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查控制台输出
print("检查最近错误日志...")
try:
    r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/webapps/ppt.pythonanywhere.com/error_logs/', headers=h, timeout=10)
    print(f"错误日志状态: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        for log in data[:5]:
            print(f"  {log.get('timestamp')}: {log.get('message', '')[:200]}")
except Exception as e:
    print(f"错误: {e}")
