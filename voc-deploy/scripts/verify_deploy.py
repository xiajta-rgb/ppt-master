import requests

print("验证部署结果...")
print()

print("[1] 测试 viewer.html...")
r = requests.get('https://ppt.pythonanywhere.com/viewer.html', timeout=30)
print(f"    状态: {r.status_code}")
if r.status_code == 200:
    if 'exportPPT' in r.text:
        print("    ✅ exportPPT 函数存在")
    else:
        print("    ❌ exportPPT 函数不存在")

print()
print("[2] 测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    params={'project': 'demo_project_intro_ppt169_20251211'},
    timeout=30
)
print(f"    状态: {r.status_code}")
if r.status_code == 500:
    print(f"    错误: {r.text[:200]}")
elif r.status_code == 404:
    print("    项目不存在")
elif r.status_code == 200:
    print(f"    ✅ 导出成功! 大小: {len(r.content)} bytes")
