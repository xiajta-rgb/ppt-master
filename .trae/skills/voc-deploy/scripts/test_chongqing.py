#!/usr/bin/env python3
"""
测试 chongqing-report 项目的完整路径
"""

import requests
from urllib.parse import quote

BASE_URL = "https://ppt.pythonanywhere.com"

# 根据 collections.js 中的 folder 值
folder = "examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final"
file = "P01_封面.svg"

# 前端构建的路径: / + encodePath(folder) + / + encodeURIComponent(file)
def encode_path(path):
    return '/'.join(quote(p, safe='') for p in path.split('/'))

path = '/' + encode_path(folder) + '/' + quote(file, safe='')

print(f"测试路径: {path}")
print(f"完整 URL: {BASE_URL}{path}")

r = requests.get(BASE_URL + path, timeout=10)
print(f"\nStatus: {r.status_code}")
print(f"Content-Type: {r.headers.get('Content-Type', 'N/A')}")
print(f"Content-Length: {len(r.content)}")

if r.status_code == 200:
    print("\n[OK] SVG 文件可访问")
else:
    print(f"\n[FAIL] Response: {r.text[:300]}")
