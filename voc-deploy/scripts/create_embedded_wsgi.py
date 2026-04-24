import os
import base64

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

# 读取 index.html 并 base64 编码
with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

index_b64 = base64.b64encode(index_content.encode('utf-8')).decode('ascii')

WSGI_TEMPLATE = f'''import os
import sys
import base64

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

INDEX_B64 = "{index_b64}"

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    # WSGI 使用 Latin-1 编码路径
    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    if path == '/' or path == '':
        content = base64.b64decode(INDEX_B64).decode('utf-8')
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
            content = '<html><body><h1>404: ' + path + '</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content.encode('utf-8')]

'''

# 保存 WSGI 文件
with open('wsgi_embedded.py', 'w', encoding='utf-8') as f:
    f.write(WSGI_TEMPLATE)

print(f"index.html 长度: {len(index_content)}")
print(f"base64 长度: {len(index_b64)}")
print(f"WSGI 长度: {len(WSGI_TEMPLATE)}")
print("已保存到 wsgi_embedded.py")
