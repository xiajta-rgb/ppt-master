#!/usr/bin/env python3
"""
检查 PythonAnywhere 上的 collections.js 内容
"""

import requests

BASE_URL = "https://ppt.pythonanywhere.com"

url = f"{BASE_URL}/public/js/collections.js"
r = requests.get(url, timeout=10)

if r.status_code == 200:
    content = r.text
    
    # 检查是否包含 chongqing-report
    if 'chongqing-report' in content:
        print("[OK] collections.js 包含 chongqing-report")
        
        # 提取 chongqing-report 相关部分
        idx = content.find('chongqing-report')
        print(f"\n找到位置: 第 {idx} 字符")
        print(f"\n上下文:")
        print(content[max(0,idx-100):idx+200])
    else:
        print("[FAIL] collections.js 不包含 chongqing-report")
    
    # 检查文件长度
    print(f"\n文件长度: {len(content)} 字符")
    
    # 检查项目数量
    import re
    ids = re.findall(r"id:\s*'([^']+)'", content)
    print(f"项目 IDs: {ids}")
else:
    print(f"[FAIL] Status: {r.status_code}")
