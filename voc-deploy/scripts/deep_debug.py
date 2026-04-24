import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

print("="*60)
print("深度排查 WSGI 问题")
print("="*60)

# 1. 确认 WSGI 文件
print("\n[1] 检查 WSGI 文件内容...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
if 'unquote' in r.text:
    print("    [OK] WSGI 包含 unquote")
else:
    print("    [X] WSGI 不含 unquote")

# 2. 通过 API 检查文件是否存在
print("\n[2] 通过 API 检查 SVG 文件是否存在...")
test_paths = [
    '/home/ppt/ppt-master/examples/TacticalClothingReport/svg_final/slide_01_cover.svg',
    '/home/ppt/ppt-master/examples/ppt169_战术服装_市场分析/svg_final/P01_封面.svg',
]

for p in test_paths:
    r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{p}', headers=headers)
    print(f"    {p.split('/')[-1]}: API={r.status_code}")

# 3. 检查 PythonAnywhere 的静态文件配置
print("\n[3] 列出 TacticalClothingReport/svg_final/ 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/TacticalClothingReport/svg_final/', headers=headers)
if r.status_code == 200:
    data = r.json()
    files = [k for k, v in data.items() if v.get('type') == 'file']
    print(f"    文件数: {len(files)}")
    print(f"    文件: {files}")

# 4. 检查 examples/TacticalClothingReport 目录结构
print("\n[4] 检查 TacticalClothingReport 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/TacticalClothingReport/', headers=headers)
if r.status_code == 200:
    data = r.json()
    print(f"    内容: {list(data.keys())}")

# 5. 检查 website 实际返回的 HTML 中 JavaScript 路径
print("\n[5] 检查网站 HTML 中的 SVG 路径...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
if r.status_code == 200:
    # 找到 renderProjects 函数中的 coverUrl
    import re
    # 找到 encodeURI 调用的内容
    matches = re.findall(r"encodeURI\(`([^`]+)`\)", r.text)
    print(f"    找到 {len(matches)} 个 encodeURI 路径")
    if matches:
        print(f"    第一个: {matches[0]}")

        # 测试这个路径
        first_path = matches[0]
        # 浏览器会如何编码这个 URL
        from urllib.parse import quote
        browser_path = quote(first_path, safe='/')
        print(f"    浏览器编码后: {browser_path}")

        # 直接用这个路径测试
        url = 'https://ppt.pythonanywhere.com/' + browser_path
        print(f"    测试 URL: {url}")
        r2 = requests.get(url, timeout=30)
        print(f"    结果: {r2.status_code}")

# 6. 检查网站是否在 /examples/ 路径上返回 404
print("\n[6] 检查 /examples/ 根路径...")
r = requests.get('https://ppt.pythonanywhere.com/examples/', timeout=30)
print(f"    /examples/ 状态: {r.status_code}")
if r.status_code == 200:
    print(f"    内容: {r.text[:200]}")
else:
    print(f"    内容: {r.text[:200]}")

print("\n" + "="*60)
