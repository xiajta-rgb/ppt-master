import requests
import time

time.sleep(20)

print("测试导出 API...")
r = requests.get(
    'https://ppt.pythonanywhere.com/api/export',
    params={'project': 'demo_project_intro_ppt169_20251211'},
    timeout=180
)

print(f"状态: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type')}")

if r.status_code == 200:
    print(f"内容长度: {len(r.content)}")
    with open('c:/Users/xmls/Documents/trae_projects/ppt-master/test_export.pptx', 'wb') as f:
        f.write(r.content)
    print("导出成功! 保存为 test_export.pptx")
elif r.status_code == 500:
    print(f"错误: {r.text[:1000]}")
else:
    print(f"响应: {r.text[:500]}")
