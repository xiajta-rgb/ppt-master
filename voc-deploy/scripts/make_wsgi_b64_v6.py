import os
import base64

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_bytes = index_html.encode('utf-8')
index_b64 = base64.b64encode(index_bytes).decode('ascii')

print(f"Index HTML: {len(index_html)} 字符")
print(f"Base64: {len(index_b64)} 字符")

WSGI_CODE = f'''import os
import base64

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

INDEX_B64 = """{index_b64}"""

def application(environ, start_response):
    marker = "B64_V6"

    path = environ.get('PATH_INFO', '/')

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

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_b64_v6.py', 'w', encoding='utf-8') as f:
    f.write(WSGI_CODE)

print(f"WSGI 文件: {len(WSGI_CODE)} 字符")
