#!/usr/bin/env python3
"""
最终完整验证 - 模拟浏览器加载 viewer.html?project=chongqing-report 的所有请求
"""

import requests
import re
from urllib.parse import quote, urljoin

BASE = "https://ppt.pythonanywhere.com"

print("=" * 60)
print("最终完整验证")
print("=" * 60)

all_ok = True

# 1. 主页面
print("\n[1] 主页面 /viewer.html?project=chongqing-report")
r = requests.get(f"{BASE}/viewer.html?project=chongqing-report", timeout=15)
if r.status_code == 200 and 'Slide Gallery' in r.text:
    print("    [OK] 页面加载成功")
else:
    print(f"    [FAIL] status={r.status_code}")
    all_ok = False

# 2. 解析 HTML 中的所有资源引用
html = r.text
css_links = re.findall(r'href="([^"]*\.css[^"]*)"', html)
js_scripts = re.findall(r'src="([^"]*\.js[^"]*)"', html)
img_srcs = re.findall(r'src="([^"]*\.(png|jpg|svg)[^"]*)"', html)

print(f"\n[2] 资源引用: {len(css_links)} CSS, {len(js_scripts)} JS, {len(img_srcs)} IMG")

# 3. 加载所有 CSS
print("\n[3] CSS 文件:")
for css in css_links:
    if css.startswith('http'):
        print(f"    [SKIP] 外部: {css[:60]}...")
        continue
    url = f"{BASE}/{css}" if not css.startswith('/') else f"{BASE}{css}"
    r = requests.get(url, timeout=10)
    ok = r.status_code == 200
    if not ok: all_ok = False
    print(f"    [{'OK' if ok else 'FAIL'}] {css}: {r.status_code} ({len(r.content)} bytes)")

# 4. 加载所有 JS
print("\n[4] JS 文件:")
for js in js_scripts:
    if js.startswith('http'):
        print(f"    [SKIP] 外部: {js[:60]}...")
        continue
    url = f"{BASE}/{js}" if not js.startswith('/') else f"{BASE}{js}"
    r = requests.get(url, timeout=10)
    ok = r.status_code == 200
    if not ok: all_ok = False
    print(f"    [{'OK' if ok else 'FAIL'}] {js}: {r.status_code} ({len(r.content)} bytes)")

# 5. API 端点
print("\n[5] API 端点:")
api_endpoints = [
    '/api/scan-projects',
    '/api/check-changes',
]
for ep in api_endpoints:
    r = requests.get(f"{BASE}{ep}", timeout=10)
    ok = r.status_code == 200
    if not ok: all_ok = False
    print(f"    [{'OK' if ok else 'FAIL'}] {ep}: {r.status_code}")

# 6. chongqing-report 项目的 SVG 文件
print("\n[6] chongqing-report SVG 文件:")
r = requests.get(f"{BASE}/api/scan-projects", timeout=10)
data = r.json()
chongqing = None
for p in data['projects']:
    if 'chongqing-report' in p.get('alias', []):
        chongqing = p
        break

if chongqing:
    folder = 'examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final'
    def encode_path(path):
        return '/'.join(quote(p, safe='') for p in path.split('/'))
    
    for slide in chongqing['slides'][:5]:
        svg_path = '/' + encode_path(folder) + '/' + quote(slide['file'], safe='')
        r = requests.get(f"{BASE}{svg_path}", timeout=10)
        ok = r.status_code == 200
        if not ok: all_ok = False
        print(f"    [{'OK' if ok else 'FAIL'}] {slide['file']}: {r.status_code} ({len(r.content)} bytes)")
else:
    print("    [FAIL] 未找到 chongqing-report")
    all_ok = False

# 7. 检查 viewer.js 中的关键逻辑
print("\n[7] viewer.js 关键逻辑:")
r = requests.get(f"{BASE}/viewer.js", timeout=10)
js = r.text
checks = [
    ("loadDynamicCollections", "loadDynamicCollections" in js),
    ("openCollection", "openCollection" in js),
    ("URL参数解析", "urlParams.get('project')" in js),
    ("alias匹配", "c.alias === collectionId" in js),
    ("id匹配", "c.id === collectionId" in js),
    ("includes匹配", "c.id.includes(collectionId)" in js),
    ("folder fallback", "examples/${p.folder}/svg_final" in js),
    ("staticData.folder", "staticData?.folder" in js),
]
for name, result in checks:
    print(f"    [{'OK' if result else 'FAIL'}] {name}")
    if not result: all_ok = False

# 8. 检查 collections.js 中的 chongqing-report
print("\n[8] collections.js chongqing-report:")
r = requests.get(f"{BASE}/js/collections.js", timeout=10)
if 'chongqing-report' in r.text:
    print("    [OK] 包含 chongqing-report")
    if "folder: 'examples/" in r.text:
        print("    [OK] folder 使用完整路径")
    else:
        print("    [WARN] folder 可能不使用完整路径")
else:
    print("    [FAIL] 不包含 chongqing-report")
    all_ok = False

# 9. 检查 index.html
print("\n[9] index.html:")
r = requests.get(f"{BASE}/", timeout=10)
if r.status_code == 200:
    print(f"    [OK] 首页可访问 ({len(r.content)} bytes)")
else:
    print(f"    [FAIL] status={r.status_code}")
    all_ok = False

# 10. 检查 Cache-Control
print("\n[10] Cache-Control:")
r = requests.get(f"{BASE}/viewer.html", timeout=10)
cc = r.headers.get('Cache-Control', '')
if 'no-cache' in cc or 'no-store' in cc:
    print(f"    [OK] {cc}")
else:
    print(f"    [WARN] {cc}")

print("\n" + "=" * 60)
if all_ok:
    print("✅ 所有测试通过！")
else:
    print("❌ 部分测试失败，请检查")
print("=" * 60)
