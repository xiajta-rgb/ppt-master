# 本地模拟 WSGI 的 INDEX_CONTENT
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

print(f"本地 index.html 长度: {len(index_html)}")

# 模拟 WSGI 的 response_headers 设置 Content-Length
content = index_html.encode('utf-8')
print(f"UTF-8 编码后长度: {len(content)}")

# 检查 em dash 位置
em_dash_pos = index_html.find('\u2014')
print(f"em dash 位置: {em_dash_pos}")

# em dash 的 UTF-8 是 \xe2\x80\x94
em_utf8 = '\u2014'.encode('utf-8')
print(f"em dash UTF-8 字节: {em_utf8}")

# 找 em dash 在字节流中的位置
for i, b in enumerate(content):
    if content[i:i+3] == em_utf8:
        print(f"em dash 在字节位置: {i}")
        break

# 检查字节 160-175
print(f"\n字节 160-175: {content[160:175]}")
print(f"字节 160-175 hex: {content[160:175].hex()}")
