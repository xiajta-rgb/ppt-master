import requests
import time

time.sleep(5)

# 测试 API 端点
print("测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    params={'project': 'demo_project_intro_ppt169_20251211'},
    timeout=60
)

print(f"状态: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type')}")

if r.status_code == 200:
    print(f"内容长度: {len(r.content)}")
    print("导出成功!")
elif r.status_code == 404:
    print(f"错误: {r.text}")
else:
    print(f"响应: {r.text[:500]}")
