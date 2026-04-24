# 服务器上的 PATH_INFO 实际上包含了 UTF-8 字节被错误解释为 Latin-1 的字符串
# 解决方案：先用 Latin-1 编码回字节，然后用 UTF-8 解码

# 模拟服务器上的 PATH_INFO（从 DEBUG 输出看到的格式）
# 这些 æ, \x88, \x98 等是 UTF-8 字节被 Latin-1 解释后的样子
path_on_server = '/examples/ppt169_\xe6\x88\x98\xe6\x9c\xaf\xe6\x9c\x8d\xe8\xa3\x85_\xe5\xb8\x82\xe5\x9c\xba\xe5\x88\x86\xe6\x9e\x90/svg_final/P01_\xe5\xb0\x81\xe9\x9d\xa2.svg'

print(f"服务器路径 (repr): {repr(path_on_server)}")

# Step 1: 用 Latin-1 编码回字节
bytes_path = path_on_server.encode('latin-1')
print(f"\n编码为 bytes: {bytes_path}")

# Step 2: 用 UTF-8 解码
try:
    correct_path = bytes_path.decode('utf-8')
    print(f"\n正确解码: {correct_path}")
    print("[OK] 这个方法有效!")
except Exception as e:
    print(f"\n错误: {e}")
