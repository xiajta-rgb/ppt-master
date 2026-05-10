#!/usr/bin/env python3
"""
重载 Web App 并验证
"""

import requests
import time

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
WEBAPP_DOMAIN = 'ppt.pythonanywhere.com'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

# 重载 Web App
print("=== 重载 Web App ===")
url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/{WEBAPP_DOMAIN}/reload/'
r = requests.post(url, headers=HEADERS, timeout=90)
print(f"重载: {r.status_code}")

time.sleep(8)

# 验证
print("\n=== 验证 ===")
test_urls = [
    ("首页", "https://ppt.pythonanywhere.com/"),
    ("Viewer", "https://ppt.pythonanywhere.com/viewer.html"),
    ("API scan", "https://ppt.pythonanywhere.com/api/scan-projects"),
    ("API check", "https://ppt.pythonanywhere.com/api/check-changes"),
    ("collections.js", "https://ppt.pythonanywhere.com/public/js/collections.js"),
    ("viewer.js", "https://ppt.pythonanywhere.com/public/viewer.js"),
    ("SVG封面", "https://ppt.pythonanywhere.com/examples/ppt169_%E9%A1%B6%E7%BA%A7%E5%92%A8%E8%AF%A2%E9%A3%8E_%E9%87%8D%E5%BA%86%E5%B8%82%E5%8C%BA%E5%9F%9F%E6%8A%A5%E5%91%8A_ppt169_20251213/svg_final/P01_%E5%B0%81%E9%9D%A2.svg"),
]

for name, url in test_urls:
    try:
        r = requests.get(url, timeout=15)
        ok = r.status_code == 200
        extra = ""
        if name == "Viewer" and ok:
            if 'window.location.search' in r.text:
                extra = " [含URL参数保留]"
            elif 'Slide Gallery' in r.text:
                extra = " [实际viewer页面]"
            else:
                extra = " [重定向页面]"
        if name == "API scan" and ok:
            data = r.json()
            projects = data.get('projects', [])
            chongqing = [p for p in projects if 'chongqing' in p['id'].lower()]
            if chongqing:
                extra = f" [含chongqing, folder={chongqing[0].get('folder','')}]"
        if name == "API check" and ok:
            data = r.json()
            extra = f" [changed={data.get('changed')}]"
        print(f"[{'OK' if ok else 'FAIL'}] {name}: {r.status_code} ({len(r.content)} bytes){extra}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")

# 特别测试: 模拟前端完整流程
print("\n=== 模拟前端完整流程 ===")

# 1. 获取 API 数据
r = requests.get("https://ppt.pythonanywhere.com/api/scan-projects", timeout=10)
api_data = r.json()
projects = api_data.get('projects', [])

# 2. 查找 chongqing-report
collection = None
for p in projects:
    if 'chongqing' in p['id'].lower():
        collection = p
        break

if collection:
    print(f"[OK] 找到项目: {collection['id']}")
    print(f"     Alias: {collection.get('alias', [])}")
    print(f"     Folder: {collection.get('folder', '')}")
    print(f"     Slides: {len(collection.get('slides', []))}")
    
    # 3. 模拟前端合并逻辑
    # 前端使用 staticData?.folder || `examples/${p.folder}/svg_final`
    # staticData 来自 collections.js
    r2 = requests.get("https://ppt.pythonanywhere.com/public/js/collections.js", timeout=10)
    if 'chongqing-report' in r2.text:
        print(f"[OK] collections.js 包含 chongqing-report")
        # 前端会使用 staticData.folder = 'examples/ppt169_.../svg_final'
        folder = 'examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final'
    else:
        # 使用 fallback
        folder = f"examples/{collection['folder']}/svg_final"
        print(f"[WARN] collections.js 不含 chongqing-report, 使用 fallback: {folder}")
    
    # 4. 测试 SVG 访问
    from urllib.parse import quote
    first_slide = collection['slides'][0]['file'] if collection.get('slides') else 'P01_封面.svg'
    def encode_path(path):
        return '/'.join(quote(p, safe='') for p in path.split('/'))
    
    svg_path = '/' + encode_path(folder) + '/' + quote(first_slide, safe='')
    svg_url = f"https://ppt.pythonanywhere.com{svg_path}"
    print(f"\n     SVG路径: {svg_path}")
    
    r3 = requests.get(svg_url, timeout=10)
    if r3.status_code == 200:
        print(f"[OK] SVG 可访问 ({len(r3.content)} bytes)")
    else:
        print(f"[FAIL] SVG 不可访问: {r3.status_code}")
else:
    print("[FAIL] 未找到 chongqing-report 项目")
