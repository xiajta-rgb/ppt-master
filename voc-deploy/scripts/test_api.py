import requests

print("测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    params={'project': 'demo_project_intro_ppt169_20251211'},
    timeout=30
)
print(f"导出状态: {r.status_code}")
print(f"响应: {r.text[:500]}")
