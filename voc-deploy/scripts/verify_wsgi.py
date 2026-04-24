import requests

print("测试 homepage 以验证 WSGI 更新...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"主页状态: {r.status_code}")
print(f"前200字符: {r.text[:200]}")

print("\n测试 /test 路径...")
r = requests.get('https://ppt.pythonanywhere.com/test', timeout=30)
print(f"/test 状态: {r.status_code}")
print(f"响应: {r.text[:100]}")
