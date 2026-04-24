import requests

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

# 检查 home/ppt 目录
print("检查 /home/ppt 目录结构...")

def list_dir(path):
    url = f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{path}'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

# 1. /home/ppt/
root = list_dir('/home/ppt/')
if root:
    print(f"\n/home/ppt/:")
    for name, info in root.items():
        print(f"  {name} ({info.get('type')})")

# 2. /home/ppt/ppt-master/
pm = list_dir('/home/ppt/ppt-master/')
if pm:
    print(f"\n/home/ppt/ppt-master/:")
    for name, info in pm.items():
        print(f"  {name} ({info.get('type')})")

# 3. 检查 /home/ppt/ 是否有其他 .html 文件
print("\n\n检查服务器根目录是否有 index.html...")
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/index.html', headers=headers)
print(f"  /home/ppt/index.html: {r.status_code}")

# 4. 模拟访问路径
print("\n\n模拟路径解析...")
project_id = 'ppt169_战术服装_市场分析'
cover = 'P01_封面.svg'
expected_path = f'/home/ppt/ppt-master/examples/{project_id}/svg_final/{cover}'
print(f"  期望的完整路径: {expected_path}")

# 检查这个路径
r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{expected_path}', headers=headers)
print(f"  API 检查结果: {r.status_code}")

# 5. 尝试直接用网站访问这个 SVG
print("\n\n直接访问 SVG (通过网站 URL)...")
svg_url = f'https://ppt.pythonanywhere.com/examples/{project_id}/svg_final/{cover}'
r = requests.get(svg_url, timeout=30)
print(f"  URL: {svg_url}")
print(f"  状态码: {r.status_code}")

# 6. 尝试一些其他路径变体
print("\n\n尝试其他路径变体...")
variants = [
    f'/home/ppt/ppt-master/examples/{project_id}/svg_final/{cover}',
    f'/home/ppt/examples/{project_id}/svg_final/{cover}',
    f'/home/ppt/ppt-master/{project_id}/svg_final/{cover}',
]
for v in variants:
    r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{v}', headers=headers)
    print(f"  {v}: {r.status_code}")
