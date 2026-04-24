# 测试 URL 解码逻辑

path = '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'

print(f"原始路径: {path}")

# 方法1: encode('latin-1').decode('utf-8')
try:
    result1 = path.encode('latin-1').decode('utf-8')
    print(f"方法1 结果: {result1}")
except Exception as e:
    print(f"方法1 错误: {e}")

# 方法2: 使用 urllib.parse
from urllib.parse import unquote
try:
    result2 = unquote(path, encoding='utf-8')
    print(f"方法2 结果: {result2}")
except Exception as e:
    print(f"方法2 错误: {e}")

# 方法3: unquote + errors='replace'
try:
    result3 = unquote(path, encoding='utf-8', errors='replace')
    print(f"方法3 结果: {result3}")
except Exception as e:
    print(f"方法3 错误: {e}")
