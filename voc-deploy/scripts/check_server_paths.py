import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

print("="*60)
print("检查服务器路径和文件结构")
print("="*60)

# 1. 检查 examples 目录
print("\n[1] 检查 examples 目录...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/', headers=headers)
if r.status_code == 200:
    data = r.json()
    dirs = [k for k, v in data.items() if v.get('type') == 'directory']
    print(f"    [OK] examples 目录存在，子目录数: {len(dirs)}")
else:
    print(f"    [X] examples 目录不存在: {r.status_code}")

# 2. 检查具体项目文件夹
project_id = 'ppt169_战术服装_市场分析'
print(f"\n[2] 检查项目文件夹: {project_id}...")
r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/{project_id}/', headers=headers)
if r.status_code == 200:
    data = r.json()
    print(f"    [OK] 项目文件夹存在")
    items = list(data.keys())[:10]
    print(f"    内容: {items}")
else:
    print(f"    [X] 项目文件夹不存在: {r.status_code}")

# 3. 检查 svg_final 目录
print(f"\n[3] 检查 svg_final 目录...")
r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/{project_id}/svg_final/', headers=headers)
if r.status_code == 200:
    data = r.json()
    files = [k for k, v in data.items() if v.get('type') == 'file']
    print(f"    [OK] svg_final 目录存在，文件数: {len(files)}")
    print(f"    前5个文件: {files[:5]}")
else:
    print(f"    [X] svg_final 目录不存在: {r.status_code}")

# 4. 检查 viewer.html
print(f"\n[4] 检查 viewer.html...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/viewer.html', headers=headers)
if r.status_code == 200:
    print(f"    [OK] viewer.html 存在，长度: {len(r.text)}")
else:
    print(f"    [X] viewer.html 不存在: {r.status_code}")

# 5. 对比本地和云端 index.html 中的项目路径
print("\n[5] 检查 index.html 中的路径配置...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/index.html', headers=headers)
if r.status_code == 200:
    content = r.text
    # 提取第一个项目的 coverUrl
    import re
    match = re.search(r"const coverUrl = encodeURI\(`examples/\$\{project\.id\}/svg_final/\$\{project\.cover\}`\);", content)
    if match:
        print("    [OK] 路径格式正确: examples/${project.id}/svg_final/${project.cover}")
    else:
        print("    [!] 路径格式可能有问题")
        # 找实际的路径
        cover_matches = re.findall(r"encodeURI\(`([^`]+)`\)", content)
        if cover_matches:
            print(f"    找到的路径: {cover_matches[:3]}")

# 6. 模拟浏览器请求，检查实际访问 SVG 会发生什么
print("\n[6] 测试实际访问 SVG 文件...")
svg_path = f'https://ppt.pythonanywhere.com/examples/{project_id}/svg_final/P01_封面.svg'
r = requests.get(svg_path, timeout=30)
print(f"    状态码: {r.status_code}")
if r.status_code == 200:
    print(f"    [OK] SVG 可访问，长度: {len(r.text)}")
else:
    print(f"    [X] SVG 返回错误")

# 7. 检查首页访问时有没有重定向或错误
print("\n[7] 检查浏览器访问首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30, allow_redirects=False)
print(f"    状态码: {r.status_code}")
print(f"    Content-Type: {r.headers.get('Content-Type')}")
print(f"    长度: {len(r.text)}")

print("\n" + "="*60)
