import os
import base64

# 读取 index.html
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# 转换为转义的字符串
index_escaped = index_html.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')

# 添加唯一标记
unique_marker = "V3_20260424_171400"

WSGI_CODE = f'''import os
import base64

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

INDEX_CONTENT = """{index_escaped}"""

def application(environ, start_response):
    # 唯一标记用于验证
    marker = "{unique_marker}"

    path = environ.get('PATH_INFO', '/')

    # WSGI 使用 Latin-1 编码路径
    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    if path == '/' or path == '':
        content = INDEX_CONTENT
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
    else:
        static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'r', encoding='utf-8') as f:
                content = f.read()
            status = '200 OK'
            if static_file.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif static_file.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif static_file.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            elif static_file.endswith('.svg'):
                content_type = 'image/svg+xml; charset=utf-8'
            else:
                content_type = 'text/plain; charset=utf-8'
        else:
            content = '<html><body><h1>404: ' + path + '</h1><p>Marker: ' + marker + '</p></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]

'''

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_v3.py', 'w', encoding='utf-8') as f:
    f.write(WSGI_CODE)

print(f"index.html 长度: {len(index_html)}")
print(f"WSGI 长度: {len(WSGI_CODE)}")
print(f"唯一标记: {unique_marker}")
print("已保存")
