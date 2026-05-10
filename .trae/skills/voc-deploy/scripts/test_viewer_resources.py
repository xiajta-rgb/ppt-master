#!/usr/bin/env python3
"""
测试 viewer.html 引用的资源路径
"""

import requests
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

# viewer.html 中引用的相对路径
RESOURCES = [
    "viewer.css",
    "viewer.js",
    "js/collections.js",
]

# 从根目录访问时的路径
ROOT_PATHS = ["/" + r for r in RESOURCES]

# 从 public 目录访问时的路径
PUBLIC_PATHS = ["/public/" + r for r in RESOURCES]

print("=" * 60)
print("测试资源路径")
print("=" * 60)

print("\n从根目录 /viewer.html 访问时的资源路径:")
for path in ROOT_PATHS:
    url = urljoin(BASE_URL, path)
    try:
        r = requests.get(url, timeout=10)
        status = "OK" if r.status_code == 200 else f"FAIL ({r.status_code})"
        print(f"  {status} - {path}")
    except Exception as e:
        print(f"  ERROR - {path}: {e}")

print("\n从 /public/viewer.html 访问时的资源路径:")
for path in PUBLIC_PATHS:
    url = urljoin(BASE_URL, path)
    try:
        r = requests.get(url, timeout=10)
        status = "OK" if r.status_code == 200 else f"FAIL ({r.status_code})"
        print(f"  {status} - {path}")
    except Exception as e:
        print(f"  ERROR - {path}: {e}")

print("\n" + "=" * 60)
print("结论: 根目录的 viewer.html 需要使用 /public/ 前缀的资源路径")
