#!/usr/bin/env python3
"""
全面测试所有资源路径
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

# 测试所有可能的资源路径
TEST_PATHS = [
    # 页面
    "/",
    "/viewer.html",
    "/public/viewer.html",
    "/public/index.html",
    
    # CSS/JS 资源
    "/public/viewer.css",
    "/public/viewer.js",
    "/public/js/collections.js",
    
    # API 端点
    "/api/scan-projects",
    "/api/projects-data",
    
    # 示例项目路径
    "/examples/ppt169_战术服装_市场分析/svg_final/P01_封面.svg",
]

def test_all():
    print("=" * 70)
    print("全面资源测试")
    print("=" * 70)
    
    success = 0
    failed = 0
    
    for path in TEST_PATHS:
        url = urljoin(BASE_URL, path)
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"[OK]   {path}")
                print(f"       Content-Length: {len(response.text)}")
                success += 1
            else:
                print(f"[FAIL] {path}")
                print(f"       Status: {status}")
                if status == 404:
                    print(f"       Response: {response.text[:200]}")
                failed += 1
                
        except Exception as e:
            print(f"[ERROR] {path}")
            print(f"        Error: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"结果: {success} 成功, {failed} 失败")
    print("=" * 70)

if __name__ == "__main__":
    test_all()
