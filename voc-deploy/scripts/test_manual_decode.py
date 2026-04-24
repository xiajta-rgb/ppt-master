import re

def decode_percent(pct_str):
    """手动解码 %XX 格式的 URL 编码"""
    result = []
    i = 0
    while i < len(pct_str):
        if pct_str[i] == '%' and i + 2 < len(pct_str):
            try:
                byte = int(pct_str[i+1:i+3], 16)
                result.append(chr(byte))
                i += 3
            except:
                result.append(pct_str[i])
                i += 1
        else:
            result.append(pct_str[i])
            i += 1
    return ''.join(result)

# 测试
test = '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
print(f"原始: {test}")
print(f"解码后: {decode_percent(test)}")

# 测试有 % 但部分解码的情况
test2 = '/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg'
print(f"\n测试2原始bytes: {test2.encode('latin-1')}")
decoded_latin1 = test2.encode('latin-1').decode('latin-1')
print(f"转回 Latin-1: {decoded_latin1}")
print(f"手动解码%: {decode_percent(decoded_latin1)}")
