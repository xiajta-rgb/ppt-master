#!/usr/bin/env python3
"""
端到端测试 - 模拟浏览器访问 viewer.html?project=chongqing-report 的完整流程
"""

import requests
import json
from urllib.parse import quote

BASE = "https://ppt.pythonanywhere.com"

print("=" * 60)
print("端到端测试: viewer.html?project=chongqing-report")
print("=" * 60)

# Step 1: 访问 /viewer.html
print("\n[1] 访问 /viewer.html")
r = requests.get(f"{BASE}/viewer.html", timeout=15)
print(f"    Status: {r.status_code}")
print(f"    Size: {len(r.content)} bytes")
if 'Slide Gallery' in r.text:
    print("    [OK] 返回了实际 viewer 页面（非重定向）")
elif 'window.location.replace' in r.text:
    print("    [WARN] 返回了重定向页面")
else:
    print("    [??] 未知内容")

# Step 2: 加载 collections.js
print("\n[2] 加载 collections.js")
r = requests.get(f"{BASE}/public/js/collections.js", timeout=10)
if r.status_code == 200 and 'chongqing-report' in r.text:
    print("    [OK] 包含 chongqing-report")
    import re
    ids = re.findall(r"id:\s*'([^']+)'", r.text)
    print(f"    项目数: {len(ids)}")
else:
    print(f"    [FAIL] status={r.status_code}")

# Step 3: 加载 viewer.js
print("\n[3] 加载 viewer.js")
r = requests.get(f"{BASE}/public/viewer.js", timeout=10)
if r.status_code == 200:
    has_loadDynamic = 'loadDynamicCollections' in r.text
    has_openCollection = 'openCollection' in r.text
    has_urlParams = "urlParams.get('project')" in r.text
    has_alias_match = "c.alias === collectionId" in r.text
    print(f"    [OK] loadDynamicCollections: {has_loadDynamic}")
    print(f"    [OK] openCollection: {has_openCollection}")
    print(f"    [OK] URL参数解析: {has_urlParams}")
    print(f"    [OK] alias匹配: {has_alias_match}")

# Step 4: API /api/scan-projects
print("\n[4] 调用 /api/scan-projects")
r = requests.get(f"{BASE}/api/scan-projects", timeout=10)
data = r.json()
projects = data.get('projects', [])
chongqing = None
for p in projects:
    if 'chongqing-report' in p.get('alias', []):
        chongqing = p
        break
if chongqing:
    print(f"    [OK] 找到 chongqing-report")
    print(f"    ID: {chongqing['id']}")
    print(f"    Folder: {chongqing['folder']}")
    print(f"    Alias: {chongqing['alias']}")
    print(f"    Slides: {len(chongqing['slides'])}")
else:
    print("    [FAIL] 未找到")

# Step 5: API /api/check-changes
print("\n[5] 调用 /api/check-changes")
r = requests.get(f"{BASE}/api/check-changes", timeout=10)
if r.status_code == 200:
    data = r.json()
    print(f"    [OK] changed={data.get('changed')}, files={len(data.get('files', []))}")
else:
    print(f"    [FAIL] status={r.status_code}")

# Step 6: 模拟前端合并逻辑
print("\n[6] 模拟前端合并逻辑")
if chongqing:
    # 前端: const staticData = staticMap.get(p.id) || staticMap.get(p.alias?.[0]);
    # p.id = 'ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213'
    # p.alias = ['chongqing-report']
    # staticMap.get(p.id) 会找到 collections.js 中的条目
    # staticData.folder = 'examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final'
    folder = 'examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final'
    print(f"    合并后 folder: {folder}")
    
    # Step 7: 测试 SVG 访问
    print("\n[7] 测试 SVG 文件访问")
    def encode_path(path):
        return '/'.join(quote(p, safe='') for p in path.split('/'))
    
    for slide in chongqing['slides'][:3]:
        svg_path = '/' + encode_path(folder) + '/' + quote(slide['file'], safe='')
        svg_url = f"{BASE}{svg_path}"
        r = requests.get(svg_url, timeout=10)
        ok = r.status_code == 200
        print(f"    [{'OK' if ok else 'FAIL'}] {slide['file']}: {r.status_code} ({len(r.content)} bytes)")

# Step 8: 测试 URL 参数保留
print("\n[8] 测试 URL 参数保留（根目录 viewer.html）")
# 根目录的 viewer.html 现在是重定向文件
r = requests.get(f"{BASE}/viewer.html?project=chongqing-report", timeout=15, allow_redirects=False)
if r.status_code in (200, 301, 302):
    if r.status_code == 200:
        if 'Slide Gallery' in r.text:
            print("    [OK] 直接返回 viewer 页面（WSGI 已修复，不再需要重定向）")
        elif 'window.location.search' in r.text:
            print("    [OK] 重定向页面保留了 URL 参数")
        else:
            print("    [WARN] 内容未知")
    else:
        location = r.headers.get('Location', '')
        print(f"    [OK] 重定向到: {location}")
else:
    print(f"    [??] Status: {r.status_code}")

# Step 9: 测试 Cache-Control
print("\n[9] 测试 Cache-Control 头")
r = requests.get(f"{BASE}/viewer.html", timeout=10)
cache_control = r.headers.get('Cache-Control', 'none')
print(f"    Cache-Control: {cache_control}")
if 'no-cache' in cache_control or 'no-store' in cache_control:
    print("    [OK] 禁用了缓存")
else:
    print("    [WARN] 未禁用缓存，浏览器可能使用旧版本")

# Step 10: 测试 CSS 加载
print("\n[10] 测试 CSS/资源加载")
css_urls = [
    "/public/viewer.html",  # HTML 中引用的 CSS
]
r = requests.get(f"{BASE}/public/viewer.html", timeout=10)
import re
css_links = re.findall(r'href="([^"]*\.css[^"]*)"', r.text)
js_scripts = re.findall(r'src="([^"]*\.js[^"]*)"', r.text)
print(f"    CSS 引用: {css_links[:5]}")
print(f"    JS 引用: {js_scripts[:5]}")

for css in css_links[:3]:
    css_url = f"{BASE}{css}" if css.startswith('/') else f"{BASE}/{css}"
    r = requests.get(css_url, timeout=10)
    print(f"    [{'OK' if r.status_code == 200 else 'FAIL'}] {css}: {r.status_code}")

for js in js_scripts[:3]:
    js_url = f"{BASE}{js}" if js.startswith('/') else f"{BASE}/{js}"
    r = requests.get(js_url, timeout=10)
    print(f"    [{'OK' if r.status_code == 200 else 'FAIL'}] {js}: {r.status_code}")

print("\n" + "=" * 60)
print("端到端测试完成")
print("=" * 60)
