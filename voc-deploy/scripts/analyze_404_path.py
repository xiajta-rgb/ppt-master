import requests
import re

# 测试 SVG 并查看响应中的路径格式
svg_url = 'https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
r = requests.get(svg_url, timeout=30)

# 提取 404 消息中的路径
match = re.search(r'<h1>404:([^<]+)</h1>', r.text)
if match:
    path_in_response = match.group(1)
    print(f"404 中的路径: {path_in_response}")

    # 检查是否包含未解码的 % 字符
    if '%' in path_in_response:
        print("[X] 路径包含 % - unquote 没有执行")
    else:
        print("[OK] 路径已解码")

    # 检查是否包含乱码
    if 'æ' in path_in_response:
        print("[X] 路径包含 æ 乱码 - 编码错误")
    else:
        print("[?] 路径看起来正常")
else:
    print(f"无法提取路径。响应: {r.text[:300]}")
