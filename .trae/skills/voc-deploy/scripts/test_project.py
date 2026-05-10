#!/usr/bin/env python3
"""
测试特定项目加载
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

print("=" * 60)
print("测试 chongqing-report 项目")
print("=" * 60)

# 1. 获取项目列表，查找 chongqing-report
print("\n1. 获取项目列表:")
r = requests.get(urljoin(BASE_URL, "/api/scan-projects"), timeout=10)
if r.status_code == 200:
    data = r.json()
    projects = data.get('projects', [])
    
    # 查找 chongqing-report
    target = None
    for p in projects:
        if p['id'] == 'chongqing-report' or 'chongqing' in p['id'].lower():
            target = p
            break
        # 检查 alias
        if 'chongqing-report' in p.get('alias', []):
            target = p
            break
    
    if target:
        print(f"   找到项目: {target['id']}")
        print(f"   Alias: {target.get('alias', [])}")
        print(f"   Slides: {len(target['slides'])}")
        if target['slides']:
            print(f"   First slide: {target['slides'][0]['file']}")
            print(f"   Last slide: {target['slides'][-1]['file']}")
    else:
        print(f"   未找到 chongqing-report")
        print(f"   可用项目:")
        for p in projects[:5]:
            print(f"     - {p['id']} (alias: {p.get('alias', [])})")
        print(f"     ... 共 {len(projects)} 个项目")
else:
    print(f"   FAIL: {r.status_code}")

# 2. 测试 projects-data
print("\n2. 获取项目详情数据:")
r = requests.get(urljoin(BASE_URL, "/api/projects-data"), timeout=10)
if r.status_code == 200:
    data = r.json()
    if 'chongqing-report' in data:
        print(f"   chongqing-report 数据:")
        print(f"   {json.dumps(data['chongqing-report'], indent=2, ensure_ascii=False)}")
    else:
        print(f"   chongqing-report 不在 projects-data 中")
        print(f"   可用 keys: {list(data.keys())[:5]}")
else:
    print(f"   FAIL: {r.status_code}")

# 3. 测试 SVG 文件访问
print("\n3. 测试 SVG 文件:")
# 根据 config.py, chongqing-report -> ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213
svg_path = "/examples/ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213/svg_final/P01_封面.svg"
r = requests.get(urljoin(BASE_URL, svg_path), timeout=10)
print(f"   Path: {svg_path}")
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   Content-Length: {len(r.content)}")
    print(f"   Content-Type: {r.headers.get('Content-Type', 'N/A')}")
else:
    print(f"   Response: {r.text[:200]}")

print("\n" + "=" * 60)
