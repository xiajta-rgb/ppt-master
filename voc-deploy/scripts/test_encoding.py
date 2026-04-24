import requests
import gzip
import io

# 测试不同的 Accept-Encoding
headers_list = [
    {'Accept-Encoding': 'identity'},
    {'Accept-Encoding': 'gzip'},
    {'Accept-Encoding': 'gzip, deflate'},
    {},
]

for i, headers in enumerate(headers_list):
    print(f"\n测试 {i+1}: {headers.get('Accept-Encoding', 'default')}")
    r = requests.get('https://ppt.pythonanywhere.com/', headers=headers, timeout=30)
    print(f"  状态: {r.status_code}")
    print(f"  长度: {len(r.text)}")
    if 'renderProjects()' in r.text:
        print("  [OK] 包含 renderProjects()")
