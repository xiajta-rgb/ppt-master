import requests

# 测试 /index.html 直接路径
urls = [
    'https://ppt.pythonanywhere.com/',
    'https://ppt.pythonanywhere.com/index.html',
    'https://ppt.pythonanywhere.com//',
]

for url in urls:
    print(f"\n测试: {url}")
    r = requests.get(url, timeout=30)
    print(f"  状态: {r.status_code}")
    print(f"  长度: {len(r.text)}")
    if 'renderProjects()' in r.text:
        print("  [OK] 包含 renderProjects()")
