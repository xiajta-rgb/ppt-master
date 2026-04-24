import os
import base64

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_b64 = base64.b64encode(index_html.encode('utf-8')).decode('ascii')

wsgi_code = r'''import os
import sys
import base64
import urllib.parse
import subprocess

LOG_FILE = '/home/ppt/pip_log.txt'

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(msg + '\n')
            f.flush()
    except:
        pass

log('=== WSGI STARTING ===')
log('sys.executable: ' + sys.executable)

try_paths = [
    '/usr/bin/pip3',
    '/usr/local/bin/pip3',
    '/usr/bin/pip',
]

pip_path = None
for p in try_paths:
    if os.path.exists(p):
        pip_path = p
        log('found pip at: ' + p)
        break

if pip_path:
    result = subprocess.run(
        [pip_path, 'install', 'python-pptx', '--user'],
        capture_output=True,
        timeout=180
    )
    log('pip install returncode: ' + str(result.returncode))
    log('stdout: ' + result.stdout.decode('utf-8', errors='replace')[:300])
    log('stderr: ' + result.stderr.decode('utf-8', errors='replace')[:300])
else:
    log('pip not found at any path')

for p in ['/home/ppt/.local/lib/python3.11/site-packages',
          '/home/ppt/.local/lib/python3.12/site-packages',
          '/usr/local/lib/python3.11/site-packages']:
    if p not in sys.path:
        sys.path.insert(0, p)
        log('added path: ' + p)

try:
    import pptx
    log('pptx imported successfully! version: ' + pptx.__version__)
except ImportError as e:
    log('pptx import failed: ' + str(e))

INDEX_B64 = """{index_b64}"""

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    log('request: ' + path)

    if path.startswith('/api/export'):
        try:
            import pptx
            status = '200 OK'
            content = ('pptx available: ' + pptx.__version__).encode('utf-8')
        except ImportError:
            status = '500 Internal Server Error'
            content = b'pptx not available'

        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(content)))
        ]
        start_response(status, response_headers)
        return [content]

    if path == '/' or path == '':
        content = base64.b64decode(INDEX_B64).decode('utf-8')
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
    else:
        static_file = '/home/ppt/ppt-master/' + path.lstrip('/')
        if os.path.exists(static_file) and os.path.isfile(static_file):
            with open(static_file, 'rb') as f:
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
            content = ('<html><body><h1>404: ' + path + '</h1></body></html>').encode('utf-8')
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'

    response_headers = [('Content-Type', content_type)]
    start_response(status, response_headers)

    if isinstance(content, str):
        return [content.encode('utf-8')]
    return [content]

'''.format(index_b64=index_b64)

with open('c:/Users/xmls/Documents/trae_projects/ppt-master/voc-deploy/scripts/wsgi_with_export.py', 'w', encoding='utf-8') as f:
    f.write(wsgi_code)

print(f"WSGI with export API created, length: {len(wsgi_code)}")
