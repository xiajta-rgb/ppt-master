#!/usr/bin/env python3
"""
调试 API 返回的项目列表
"""

import requests

r = requests.get("https://ppt.pythonanywhere.com/api/scan-projects", timeout=10)
data = r.json()
projects = data.get('projects', [])

print(f"项目总数: {len(projects)}")
print("\n所有项目 ID:")
for p in projects:
    alias = p.get('alias', [])
    print(f"  - {p['id']}  alias={alias}")

# 搜索 chongqing
print("\n搜索 chongqing:")
for p in projects:
    id_lower = p['id'].lower()
    alias_str = str(p.get('alias', [])).lower()
    if 'chongqing' in id_lower or 'chongqing' in alias_str or '重庆' in p['id']:
        print(f"  [FOUND] {p['id']}")
        print(f"    alias: {p.get('alias', [])}")
        print(f"    folder: {p.get('folder', '')}")
        print(f"    slides: {len(p.get('slides', []))}")
