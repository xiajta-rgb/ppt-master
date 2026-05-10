#!/usr/bin/env python3
"""
测试 PythonAnywhere 部署状态
检查 viewer.html 和相关文件是否可访问
"""

import requests
import sys
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

# 测试路径列表
TEST_PATHS = [
    "/",
    "/viewer.html",
    "/public/viewer.html",
    "/public/viewer.css",
    "/public/viewer.js",
    "/public/js/collections.js",
    "/public/index.html",
]

def test_path(path):
    """测试单个路径"""
    url = urljoin(BASE_URL, path)
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        content_length = len(response.text)
        
        if status == 200:
            print(f"[OK] {path}")
            print(f"     Status: {status}, Content-Length: {content_length}")
            if "viewer" in path and content_length < 100:
                print(f"     WARNING: Content too short, might be redirect or error")
                print(f"     Content: {response.text[:200]}")
        elif status == 404:
            print(f"[FAIL] {path}")
            print(f"     Status: {status} - Not Found")
            # 打印 404 页面内容以便诊断
            print(f"     Response: {response.text[:300]}")
        else:
            print(f"[WARN] {path}")
            print(f"     Status: {status}, Content-Length: {content_length}")
            
        return status == 200
    except Exception as e:
        print(f"[ERROR] {path}")
        print(f"     Error: {e}")
        return False

def main():
    print("=" * 60)
    print("PythonAnywhere 部署测试")
    print("=" * 60)
    print(f"\nBase URL: {BASE_URL}\n")
    
    success_count = 0
    total_count = len(TEST_PATHS)
    
    for path in TEST_PATHS:
        if test_path(path):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"测试结果: {success_count}/{total_count} 通过")
    print("=" * 60)
    
    if success_count < total_count:
        print("\n建议检查:")
        print("1. WSGI 文件中的 STATIC_DIR 配置")
        print("2. 文件是否已同步到 PythonAnywhere")
        print("3. 文件路径是否正确")

if __name__ == "__main__":
    main()
