import requests

print("测试 viewer.html...")
r = requests.get('https://ppt.pythonanywhere.com/viewer.html', timeout=30)
print(f"状态: {r.status_code}")
print(f"前200字符: {r.text[:200]}")
