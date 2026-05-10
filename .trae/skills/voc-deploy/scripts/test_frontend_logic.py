#!/usr/bin/env python3
"""
模拟前端 JavaScript 的数据合并逻辑
"""

import requests
import json

BASE_URL = "https://ppt.pythonanywhere.com"

# 1. 获取 API 数据
print("1. 获取 /api/scan-projects:")
r = requests.get(f"{BASE_URL}/api/scan-projects", timeout=10)
api_data = r.json()
api_projects = api_data.get('projects', [])
print(f"   API 返回 {len(api_projects)} 个项目")

# 2. 获取 collections.js 中的静态数据（模拟）
# 这里我们直接检查 chongqing-report
chongqing_api = None
for p in api_projects:
    if p['id'] == 'chongqing-report' or p.get('alias') == ['chongqing-report'] or 'chongqing' in p['id'].lower():
        chongqing_api = p
        break
    # 检查 alias 列表
    if 'chongqing-report' in p.get('alias', []):
        chongqing_api = p
        break

if chongqing_api:
    print(f"\n2. 找到 chongqing-report:")
    print(f"   ID: {chongqing_api['id']}")
    print(f"   Alias: {chongqing_api.get('alias', [])}")
    print(f"   Folder: {chongqing_api.get('folder', '')}")
    print(f"   Slides: {len(chongqing_api.get('slides', []))}")
    if chongqing_api.get('slides'):
        print(f"   First slide: {chongqing_api['slides'][0]}")
else:
    print("\n2. [FAIL] 未找到 chongqing-report")
    print("   最接近的项目:")
    for p in api_projects:
        if 'chongqing' in p['id'].lower() or 'chongqing' in str(p.get('alias', [])).lower():
            print(f"     - {p['id']} (alias: {p.get('alias', [])})")

# 3. 测试前端查找逻辑
print("\n3. 模拟前端查找逻辑:")
print("   collections.find(c => c.alias === 'chongqing-report')")

# 检查 collections.js 中的 alias 值
r = requests.get(f"{BASE_URL}/public/js/collections.js", timeout=10)
content = r.text

# 查找 chongqing-report 的 alias 定义
import re
# 查找 alias: 'chongqing-report'
alias_matches = re.findall(r"alias:\s*'([^']*)'.*?title:\s*'([^']*)'", content)
print(f"\n   collections.js 中的 alias 映射:")
for alias, title in alias_matches:
    if 'chongqing' in alias.lower() or 'chongqing' in title.lower():
        print(f"     alias: '{alias}' -> title: '{title}'")

print("\n" + "=" * 60)
print("结论: 如果 API 和 collections.js 都包含 chongqing-report，")
print("      问题可能出在前端 JavaScript 执行或浏览器缓存")
