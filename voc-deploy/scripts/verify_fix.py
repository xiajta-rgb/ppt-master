import requests
import urllib.parse

print("验证 WSGI 并测试中文路径...")

# 1. 确认 WSGI 已更新
headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=headers)
if r.status_code == 200:
    if 'from urllib.parse import unquote' in r.text:
        print("[OK] WSGI 已包含 URL 解码")
    else:
        print("[X] WSGI 未更新")
        print(r.text[-500:])
else:
    print(f"[X] 无法获取 WSGI: {r.status_code}")

# 2. 测试中文 SVG 路径
project_id = 'ppt169_战术服装_市场分析'
cover = 'P01_封面.svg'
encoded_id = urllib.parse.quote(project_id)
encoded_cover = urllib.parse.quote(cover)
url = f'https://ppt.pythonanywhere.com/examples/{encoded_id}/svg_final/{encoded_cover}'

print(f"\n测试 SVG 访问: {url}")
r = requests.get(url, timeout=30)
print(f"状态: {r.status_code}")
if r.status_code == 200:
    print(f"[OK] SVG 可访问! 长度: {len(r.text)}")
else:
    print(f"[X] SVG 返回: {r.status_code}")

# 3. 测试首页
print(f"\n测试首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
if r.status_code == 200 and '亚马逊战术服装' in r.text:
    print("[OK] 首页包含正确内容")
else:
    print(f"[X] 首页状态异常")
