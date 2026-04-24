import requests

r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"实际长度: {len(r.text)}")

# 检查调试信息中的 SIZE
import re
size_match = re.search(r'SIZE=(\d+)', r.text)
if size_match:
    print(f"文件实际大小: {size_match.group(1)}")
