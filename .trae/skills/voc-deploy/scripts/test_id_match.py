#!/usr/bin/env python3
"""
检查 API 返回的 ID 和 collections.js 中的 ID 匹配情况
"""

import requests
import re

BASE_URL = "https://ppt.pythonanywhere.com"

# 获取 API 数据
r = requests.get(f"{BASE_URL}/api/scan-projects", timeout=10)
api_data = r.json()
api_ids = [p['id'] for p in api_data['projects']]

# 获取 collections.js 中的 ID
r = requests.get(f"{BASE_URL}/public/js/collections.js", timeout=10)
content = r.text
js_ids = re.findall(r"id:\s*'([^']+)'", content)

print("API IDs:")
for id in api_ids:
    print(f"  - {id}")

print("\ncollections.js IDs:")
for id in js_ids:
    print(f"  - {id}")

print("\n匹配检查:")
for api_id in api_ids:
    if api_id in js_ids:
        print(f"  [OK] {api_id}")
    else:
        print(f"  [FAIL] {api_id} - 不在 collections.js 中")

# 特别检查 chongqing-report
print("\nchongqing-report 检查:")
chongqing_api = [p for p in api_data['projects'] if 'chongqing' in p['id'].lower()][0]
print(f"  API ID: {chongqing_api['id']}")
print(f"  API Alias: {chongqing_api.get('alias', [])}")
print(f"  在 collections.js 中: {'是' if chongqing_api['id'] in js_ids else '否'}")
