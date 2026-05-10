#!/usr/bin/env python3
"""
检查 chongqing-report 的完整数据流
"""

import requests
import re

BASE_URL = "https://ppt.pythonanywhere.com"

# 获取 API 数据
r = requests.get(f"{BASE_URL}/api/scan-projects", timeout=10)
api_data = r.json()

# 查找 chongqing-report
chongqing_api = None
for p in api_data['projects']:
    if 'chongqing' in p['id'].lower() or 'chongqing-report' in str(p.get('alias', [])):
        chongqing_api = p
        break

if chongqing_api:
    print("API 中的 chongqing-report:")
    print(f"  ID: {chongqing_api['id']}")
    print(f"  Alias: {chongqing_api.get('alias', [])}")
    print(f"  Folder: {chongqing_api.get('folder', 'N/A')}")
    print(f"  Slides count: {len(chongqing_api.get('slides', []))}")
    if chongqing_api.get('slides'):
        print(f"  First slide: {chongqing_api['slides'][0]}")
else:
    print("[FAIL] 未找到 chongqing-report")

# 获取 collections.js
r = requests.get(f"{BASE_URL}/public/js/collections.js", timeout=10)
content = r.text

# 提取 chongqing 相关部分
idx = content.find('chongqing-report')
if idx >= 0:
    print("\ncollections.js 中的 chongqing-report:")
    # 向前找到 id 定义
    start = content.rfind('id:', 0, idx)
    # 向后找到下一个项目的开始
    end = content.find('},\n    {', idx)
    if end == -1:
        end = content.find('}\n];', idx)
    
    block = content[start:end+1]
    print(block[:500])
else:
    print("\n[FAIL] collections.js 中未找到 chongqing-report")
