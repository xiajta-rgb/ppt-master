import requests

h = {'Authorization': 'Token c061620aaca584d026e45dc2baede02bd46ae0de'}
r = requests.get('https://www.pythonanywhere.com/api/v0/user/ppt/files/path/var/www/ppt_pythonanywhere_com_wsgi.py', headers=h)

# 查找 em dash 的 UTF-8 序列
content = r.text
# em dash 是 \u2014 或 \xe2\x80\x94
pos = content.find('\u2014')
print(f"em dash (unicode) 位置: {pos}")

# 检查那个位置附近的字节
if pos > 0:
    print(f"附近内容: {repr(content[pos-10:pos+10])}")

# 检查 \xe2\x80\x94
pos2 = content.find('\xe2\x80\x94')
print(f"em dash (utf8) 位置: {pos2}")

# 保存到文件对比
with open('wsgi_api.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print(f"\nWSGI API 内容已保存，长度: {len(r.text)}")
