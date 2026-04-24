import requests
import urllib.parse

headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}

print("测试不同 URL 编码方式访问 SVG...")

# 1. URL 编码的中文路径
project_id = 'ppt169_战术服装_市场分析'
cover = 'P01_封面.svg'

# 方式1: 直接中文 (浏览器通常这样)
url1 = f'https://ppt.pythonanywhere.com/examples/{project_id}/svg_final/{cover}'
print(f"\n[1] 直接中文路径:")
print(f"    URL: {url1}")
r = requests.get(url1, timeout=30)
print(f"    状态: {r.status_code}")

# 方式2: URL 编码
encoded_id = urllib.parse.quote(project_id)
encoded_cover = urllib.parse.quote(cover)
url2 = f'https://ppt.pythonanywhere.com/examples/{encoded_id}/svg_final/{encoded_cover}'
print(f"\n[2] URL 编码路径:")
print(f"    URL: {url2}")
r = requests.get(url2, timeout=30)
print(f"    状态: {r.status_code}")

# 方式3: 检查 index.html 能否被正常加载 (ASCII 路径)
print(f"\n[3] 测试 index.html 访问:")
r = requests.get('https://ppt.pythonanywhere.com/index.html', timeout=30)
print(f"    状态: {r.status_code}")
print(f"    长度: {len(r.text)}")

# 方式4: 检查 examples 目录能否列出 (目录访问)
print(f"\n[4] 测试 examples 目录 (可能返回 HTML 列表):")
r = requests.get('https://ppt.pythonanywhere.com/examples/', timeout=30)
print(f"    状态: {r.status_code}")
print(f"    长度: {len(r.text)}")
if r.status_code == 200:
    if 'ppt169' in r.text:
        print("    [OK] examples 内容包含项目")
    else:
        print("    [X] examples 内容不包含项目")

# 方式5: 测试纯 ASCII 路径
print(f"\n[5] 测试纯 ASCII SVG 路径:")
# 找服务器上是否有纯 ASCII 命名的 SVG
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/', headers=headers)
if r.status_code == 200:
    data = r.json()
    # 找一个 ASCII 命名的项目
    for name in data.keys():
        if name.isascii():
            print(f"    找到 ASCII 项目: {name}")
            # 检查它的 svg 文件
            r2 = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path/home/ppt/ppt-master/examples/{name}/svg_final/', headers=headers)
            if r2.status_code == 200:
                svg_data = r2.json()
                svg_files = [k for k, v in svg_data.items() if k.endswith('.svg')]
                if svg_files:
                    test_svg = svg_files[0]
                    print(f"    测试 SVG: {test_svg}")
                    # 尝试通过网站访问
                    url = f'https://ppt.pythonanywhere.com/examples/{name}/svg_final/{test_svg}'
                    r3 = requests.get(url, timeout=30)
                    print(f"    网站访问状态: {r3.status_code}")
                    break
