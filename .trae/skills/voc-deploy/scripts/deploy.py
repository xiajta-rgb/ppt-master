#!/usr/bin/env python3
"""
PPT Master Deploy - 部署脚本
包含导出功能
"""

import requests
import uuid

API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
USERNAME = 'ppt'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'

WSGI_CONTENT = '''import os
import sys
import base64
import urllib.parse
import subprocess

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR

SCRIPTS_DIR = os.path.join(PROJECT_DIR, 'skills', 'ppt-master', 'scripts')
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

LOG_FILE = '/home/ppt/wsgi_export.log'

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            import datetime
            f.write(datetime.datetime.now().isoformat() + ' ' + msg + '\\n')
            f.flush()
    except:
        pass

log('WSGI starting')

SVG_TO_PPTX_OK = False
try:
    from svg_to_pptx import create_pptx_with_native_svg
    from svg_to_pptx.pptx_discovery import find_svg_files
    SVG_TO_PPTX_OK = True
    log('svg_to_pptx imports OK')
except Exception as e:
    log('svg_to_pptx import failed: ' + str(e))

INDEX_FILE = os.path.join(STATIC_DIR, 'index.html')
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        INDEX_CONTENT = f.read()
else:
    INDEX_CONTENT = '<html><body><h1>index.html not found</h1></body></html>'

def lazy_import_pptx():
    try:
        import pptx
        return True, None
    except ImportError:
        log('pptx not available')

        for p in ['/home/ppt/.local/lib/python3.11/site-packages',
                  '/home/ppt/.local/lib/python3.12/site-packages',
                  '/usr/local/lib/python3.11/site-packages',
                  '/usr/lib/python3/dist-packages']:
            if p not in sys.path:
                sys.path.insert(0, p)
                log('added path: ' + p)

        try:
            import pptx
            return True, None
        except ImportError:
            pass

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'python-pptx'],
                capture_output=True,
                timeout=300,
                env=os.environ.copy()
            )
            log('pip returncode: ' + str(result.returncode))
            if result.returncode == 0:
                try:
                    import importlib
                    importlib.invalidate_caches()
                    import pptx
                    return True, None
                except:
                    pass
            return False, 'pip failed'
        except Exception as e:
            log('exception: ' + str(e))
            return False, str(e)

    return False, 'unknown error'

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')

    if '%' in path or any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass

    log('request: ' + path)

    if path.startswith('/api/export'):
        ok, err = lazy_import_pptx()
        if not ok:
            status = '500 Internal Server Error'
            err_str = str(err)[:500] if err else 'unknown'
            content = ('{"error": "Import failed: ' + err_str.replace('\\\\', '\\\\\\\\').replace('"', '\\\\"') + '"}').encode('utf-8')
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(content)))
            ]
            start_response(status, response_headers)
            return [content]

        if not SVG_TO_PPTX_OK:
            status = '500 Internal Server Error'
            content = b'{"error": "svg_to_pptx not available"}'
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(content)))
            ]
            start_response(status, response_headers)
            return [content]

        query = environ.get('QUERY_STRING', '')
        params = urllib.parse.parse_qs(query)
        project_id = params.get('project', [''])[0]

        if not project_id:
            status = '400 Bad Request'
            content = b'{"error": "Missing project parameter"}'
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(content)))
            ]
            start_response(status, response_headers)
            return [content]

        project_path = os.path.join(PROJECT_DIR, 'examples', project_id)
        svg_final_dir = os.path.join(project_path, 'svg_final')

        if not os.path.exists(svg_final_dir):
            status = '404 Not Found'
            err_msg = '{"error": "Project not found: ' + project_id + '"}'
            content = err_msg.encode('utf-8')
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(content)))
            ]
            start_response(status, response_headers)
            return [content]

        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                svg_files = find_svg_files(Path(svg_final_dir), None)
                if not svg_files:
                    raise Exception('No SVG files found')

                output_path = Path(tmpdir) / (project_id + '.pptx')

                result = create_pptx_with_native_svg(
                    svg_files=svg_files,
                    output_path=output_path,
                    canvas_format=None,
                    verbose=False,
                    transition='fade',
                    transition_duration=0.5,
                    use_compat_mode=True,
                    notes=None,
                    enable_notes=True,
                    use_native_shapes=True,
                )

                if not result or not output_path.exists():
                    raise Exception('PPTX creation failed')

                with open(output_path, 'rb') as f:
                    pptx_content = f.read()

                status = '200 OK'
                response_headers = [
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
                    ('Content-Disposition', 'attachment; filename="' + project_id + '.pptx"'),
                    ('Content-Length', str(len(pptx_content)))
                ]
                start_response(status, response_headers)
                return [pptx_content]

            except Exception as e:
                status = '500 Internal Server Error'
                err_msg = '{"error": "' + str(e) + '"}'
                content = err_msg.encode('utf-8')
                response_headers = [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(content)))
                ]
                start_response(status, response_headers)
                return [content]

    if path == '/' or path == '':
        content = INDEX_CONTENT
        status = '200 OK'
        content_type = 'text/html; charset=utf-8'
    else:
        static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
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
            elif static_file.endswith('.png'):
                content_type = 'image/png'
            elif static_file.endswith('.jpg') or static_file.endswith('.jpeg'):
                content_type = 'image/jpeg'
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

'''

def upload_wsgi():
    boundary = uuid.uuid4().hex
    headers = {
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    body = f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="wsgi.py"\r\nContent-Type: text/plain\r\n\r\n{WSGI_CONTENT}\r\n--{boundary}--\r\n'

    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
    resp = requests.post(url, headers=headers, data=body.encode('utf-8'), timeout=60)
    return resp.status_code in (200, 201)

def reload_webapp():
    url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/ppt.pythonanywhere.com/reload/'
    headers = {'Authorization': f'Token {API_TOKEN}'}
    resp = requests.post(url, headers=headers, timeout=30)
    return resp.status_code == 200

def verify():
    import time
    time.sleep(3)
    try:
        resp = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
        if resp.status_code == 200:
            print("[OK] 网站验证成功!")
            return True
    except Exception as e:
        print(f"[!] 验证异常: {e}")
    print("[!] 验证完成，请手动检查网站")
    return True

def main():
    print("="*50)
    print("PPT Master Deploy (with Export API)")
    print("="*50)

    print("\n[Step 1] 上传 WSGI...")
    if upload_wsgi():
        print("[OK] WSGI 上传成功")
    else:
        print("[X] WSGI 上传失败")
        return

    print("\n[Step 2] Reload Webapp...")
    if reload_webapp():
        print("[OK] Reload 成功")
    else:
        print("[!] Reload 失败，请手动Reload")

    print("\n[Step 3] 验证网站...")
    verify()

    print("\n" + "="*50)
    print("部署完成!")
    print("="*50)
    print("\n访问: https://ppt.pythonanywhere.com/")
    print("导出API: https://ppt.pythonanywhere.com/api/export?project=项目名")

if __name__ == '__main__':
    main()
