import requests

# 你选择的 HTML 中的图片 src
img_src = "examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg"

print(f"图片 src: {img_src}")
print(f"完整 URL: https://ppt.pythonanywhere.com/{img_src}")

# 测试这个精确的 URL
r = requests.get(f'https://ppt.pythonanywhere.com/{img_src}', timeout=30)
print(f"\n状态码: {r.status_code}")

# 用 API 检查文件是否存在
headers = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}
file_path = '/home/ppt/ppt-master/examples/ppt169_战术服装_市场分析/svg_final/P01_封面.svg'
r2 = requests.get(f'https://www.pythonanywhere.com/api/v0/user/ppt/files/path{file_path}', headers=headers)
print(f"\nAPI 检查文件存在: {r2.status_code}")

# 解码 URL 看看
from urllib.parse import unquote
decoded = unquote(img_src)
print(f"\n解码后路径: {decoded}")

# 测试解码后的路径
r3 = requests.get(f'https://ppt.pythonanywhere.com/{decoded}', timeout=30)
print(f"解码后 URL 状态: {r3.status_code}")
