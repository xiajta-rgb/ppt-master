#!/usr/bin/env python3
"""
测试 API 端点数据返回
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "https://ppt.pythonanywhere.com"

API_ENDPOINTS = [
    "/api/scan-projects",
    "/api/projects-data",
]

def test_api(endpoint):
    """测试API端点"""
    url = urljoin(BASE_URL, endpoint)
    try:
        response = requests.get(url, timeout=10)
        print(f"\n{'='*60}")
        print(f"API: {endpoint}")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response (JSON):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
            except:
                print(f"Response (Text):")
                print(response.text[:1000])
        else:
            print(f"Error Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"\n[ERROR] {endpoint}")
        print(f"Error: {e}")

def main():
    print("测试 API 端点数据")
    print("="*60)
    
    for endpoint in API_ENDPOINTS:
        test_api(endpoint)
    
    print("\n" + "="*60)
    print("测试完成")

if __name__ == "__main__":
    main()
