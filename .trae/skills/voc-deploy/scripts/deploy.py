#!/usr/bin/env python3
"""
PPT Master Deploy - 统一部署脚本
上传正确的 WSGI 并重载 Web 应用
"""

import subprocess
import time
import requests
import sys
import ssl
from pathlib import Path

import urllib3

class TLS12Adapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

tls12_adapter = TLS12Adapter()

USERNAME = 'ppt'
API_TOKEN = 'c061620aaca584d026e45dc2baede02bd46ae0de'
HOST = 'www.pythonanywhere.com'
WEBAPP_DOMAIN = 'ppt.pythonanywhere.com'
WSGI_FILE_PATH = '/var/www/ppt_pythonanywhere_com_wsgi.py'
HEADERS = {'Authorization': f'Token {API_TOKEN}'}

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent

WSGI_CONTENT = '''import os
import sys
import json
import time
import urllib.parse

PROJECT_DIR = '/home/ppt/ppt-master'
STATIC_DIR = PROJECT_DIR
EXAMPLES_DIR = os.path.join(PROJECT_DIR, 'examples')
PUBLIC_DIR = os.path.join(PROJECT_DIR, 'public')

LOG_FILE = '/home/ppt/wsgi_export.log'

BLOCKED_EXTENSIONS = {'.py', '.pyc', '.pyo', '.env', '.sh', '.bash', '.cfg', '.ini', '.toml', '.yaml', '.yml', '.log', '.sql', '.db', '.sqlite', '.git', '.gitignore', '.htaccess', '.dockerfile'}

BLOCKED_PREFIXES = {'.git', '.env', '__pycache__', 'node_modules', '.trae', '.vscode', '.idea'}

PROJECT_ALIASES = {
    'git-intro': 'ppt169_像素风_git_introduction',
    'tactical-clothing': 'ppt169_战术服装_市场分析',
    'yili-feng': 'ppt169_易理风_地山谦卦深度研究',
    'chan-yi-feng': 'ppt169_禅意风_金刚经第一品研究',
    'demo-project': 'demo_project_intro_ppt169_20251211',
    'dark-tech': 'ppt169_general_dark_tech_claude_code_auto_mode',
    'claude-code-auto-mode': 'ppt169_general_dark_tech_claude_code_auto_mode',
    'google-annual': 'ppt169_谷歌风_google_annual_report',
    'debug六步法': 'ppt169_通用灵活+代码_debug六步法',
    'ai-programming-tools': 'ppt169_通过灵活+代码_三大AI编程神器横向对比',
    'attachment-therapy': 'ppt169_顶级咨询风_心理治疗中的依恋',
    'chongqing-report': 'ppt169_顶级咨询风_重庆市区域报告_ppt169_20251213',
    'ganzi-economy': 'ppt169_顶级咨询风_甘孜州经济财政分析',
    'ai-agent-anthropic': 'ppt169_顶级咨询风_构建有效AI代理_Anthropic',
    'nam-ou-hydro': 'ppt169_高端咨询风_南欧江水电站战略评估',
    'car-certification': 'ppt169_高端咨询风_汽车认证五年战略规划',
    'customer-loyalty': 'ppt169_麦肯锡风_kimsoong_customer_loyalty',
    'tactical-clothing-report': 'TacticalClothingReport',
    'astrology-archetypes': 'ppt169_宇宙深空风_占星学五大底层人性原型',
}

SCAN_CACHE_TTL = 60
_scan_cache = {'data': None, 'timestamp': 0}
_last_reload_time = time.time()
_file_watch_initialized = False
_file_watch_cache = {}

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            import datetime
            f.write(datetime.datetime.now().isoformat() + ' ' + msg + '\\n')
            f.flush()
    except:
        pass

log('WSGI starting')

def get_file_mtime(file_path):
    try:
        return os.path.getmtime(file_path)
    except:
        return 0

def scan_projects():
    global _scan_cache
    now = time.time()
    if _scan_cache['data'] and (now - _scan_cache['timestamp']) < SCAN_CACHE_TTL:
        return _scan_cache['data']
    
    projects = []
    if os.path.exists(EXAMPLES_DIR):
        for item in os.listdir(EXAMPLES_DIR):
            item_path = os.path.join(EXAMPLES_DIR, item)
            if os.path.isdir(item_path):
                svg_final = os.path.join(item_path, 'svg_final')
                slides = []
                if os.path.exists(svg_final):
                    for svg_file in sorted(os.listdir(svg_final)):
                        if svg_file.endswith('.svg'):
                            svg_path = os.path.join(svg_final, svg_file)
                            slides.append({'file': svg_file, 'mtime': get_file_mtime(svg_path)})
                projects.append({
                    'id': item,
                    'folder': item,
                    'slides': slides,
                    'alias': [k for k, v in PROJECT_ALIASES.items() if v == item]
                })
    
    result = json.dumps({'projects': projects, 'timestamp': now}, ensure_ascii=False)
    _scan_cache = {'data': result, 'timestamp': now}
    return result

def check_changes():
    global _file_watch_cache, _file_watch_initialized
    current_files = {}
    if os.path.exists(EXAMPLES_DIR):
        for project_dir_name in os.listdir(EXAMPLES_DIR):
            project_dir = os.path.join(EXAMPLES_DIR, project_dir_name)
            if os.path.isdir(project_dir):
                svg_final = os.path.join(project_dir, 'svg_final')
                if os.path.exists(svg_final):
                    for svg_file in os.listdir(svg_final):
                        if svg_file.endswith('.svg'):
                            key = os.path.join(project_dir_name, 'svg_final', svg_file)
                            current_files[key] = get_file_mtime(os.path.join(svg_final, svg_file))
    
    if not _file_watch_initialized:
        _file_watch_cache = current_files
        _file_watch_initialized = True
        return []
    
    changed = [k for k, v in current_files.items() if k not in _file_watch_cache or _file_watch_cache[k] != v]
    _file_watch_cache = current_files
    if changed:
        _scan_cache['data'] = None
    return changed

def get_projects_data():
    data_file = os.path.join(EXAMPLES_DIR, 'projects_data.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return f.read()
    return '{}'

def resolve_path(path):
    if '%' in path:
        try:
            path = urllib.parse.unquote(path)
        except:
            pass
    if any(ord(c) > 127 for c in path):
        try:
            path = path.encode('latin-1').decode('utf-8')
        except:
            pass
    return path

def is_path_safe(path):
    resolved = os.path.normpath(path)
    resolved = resolved.replace('\\\\', '/')
    if '..' in resolved.split('/'):
        return False
    for part in resolved.split('/'):
        if part in BLOCKED_PREFIXES:
            return False
    _, ext = os.path.splitext(resolved)
    if ext.lower() in BLOCKED_EXTENSIONS:
        return False
    return True

def read_file_safe(file_path):
    try:
        real = os.path.realpath(file_path)
        if not real.startswith(os.path.realpath(STATIC_DIR)):
            return None
    except:
        return None
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except:
        return None

def get_content_type(file_path):
    if file_path.endswith('.html'):
        return 'text/html; charset=utf-8'
    elif file_path.endswith('.css'):
        return 'text/css; charset=utf-8'
    elif file_path.endswith('.js'):
        return 'application/javascript; charset=utf-8'
    elif file_path.endswith('.svg'):
        return 'image/svg+xml; charset=utf-8'
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif file_path.endswith('.json'):
        return 'application/json; charset=utf-8'
    elif file_path.endswith('.ico'):
        return 'image/x-icon'
    elif file_path.endswith('.woff') or file_path.endswith('.woff2'):
        return 'font/woff2'
    elif file_path.endswith('.ttf'):
        return 'font/ttf'
    else:
        return 'application/octet-stream'

def not_found(path):
    return (b'<html><body><h1>404</h1></body></html>', '404 Not Found', 'text/html; charset=utf-8')

def serve_static_file(path):
    if not is_path_safe(path):
        return not_found(path)
    
    static_file = os.path.join(STATIC_DIR, path.lstrip('/'))
    content = read_file_safe(static_file)
    if content is not None:
        return (content, '200 OK', get_content_type(static_file))
    
    public_file = os.path.join(PUBLIC_DIR, path.lstrip('/'))
    content = read_file_safe(public_file)
    if content is not None:
        return (content, '200 OK', get_content_type(public_file))
    
    return not_found(path)

def application(environ, start_response):
    try:
        path = environ.get('PATH_INFO', '/')
        path = resolve_path(path)
        
        log('request: ' + path[:200])
        
        if path == '/' or path == '':
            content = read_file_safe(os.path.join(PUBLIC_DIR, 'index.html'))
            if content:
                status = '200 OK'
                content_type = 'text/html; charset=utf-8'
            else:
                content, status, content_type = not_found(path)
        
        elif path == '/viewer.html':
            content = read_file_safe(os.path.join(PUBLIC_DIR, 'viewer.html'))
            if content:
                status = '200 OK'
                content_type = 'text/html; charset=utf-8'
            else:
                content, status, content_type = not_found(path)
        
        elif path == '/index.html':
            content = read_file_safe(os.path.join(PUBLIC_DIR, 'index.html'))
            if content:
                status = '200 OK'
                content_type = 'text/html; charset=utf-8'
            else:
                content, status, content_type = not_found(path)
        
        elif path == '/api/scan-projects':
            content = scan_projects().encode('utf-8')
            status = '200 OK'
            content_type = 'application/json; charset=utf-8'
        
        elif path == '/api/projects-data':
            content = get_projects_data().encode('utf-8')
            status = '200 OK'
            content_type = 'application/json; charset=utf-8'
        
        elif path == '/api/check-changes':
            changed = check_changes()
            content = json.dumps({
                'changed': len(changed) > 0,
                'files': changed,
                'timestamp': _last_reload_time
            }, ensure_ascii=False).encode('utf-8')
            status = '200 OK'
            content_type = 'application/json; charset=utf-8'
        
        elif path == '/api/save-svg' and environ.get('REQUEST_METHOD') == 'POST':
            try:
                body_len = int(environ.get('CONTENT_LENGTH', 0))
                if body_len > 0 and body_len < 10 * 1024 * 1024:
                    body = environ['wsgi.input'].read(body_len)
                    data = json.loads(body.decode('utf-8'))
                    folder = data.get('folder', '')
                    filename = data.get('file', '')
                    svg_content = data.get('content', '')
                    
                    if not folder or not filename or not svg_content:
                        content = json.dumps({'success': False, 'error': 'Missing fields'}).encode('utf-8')
                    elif not filename.endswith('.svg'):
                        content = json.dumps({'success': False, 'error': 'Invalid file type'}).encode('utf-8')
                    elif '..' in folder or '..' in filename:
                        content = json.dumps({'success': False, 'error': 'Invalid path'}).encode('utf-8')
                    else:
                        save_dir = os.path.join(PROJECT_DIR, folder)
                        save_path = os.path.join(save_dir, filename)
                        real_save = os.path.realpath(save_path)
                        if not real_save.startswith(os.path.realpath(EXAMPLES_DIR)):
                            content = json.dumps({'success': False, 'error': 'Access denied'}).encode('utf-8')
                        else:
                            os.makedirs(save_dir, exist_ok=True)
                            with open(save_path, 'w', encoding='utf-8') as f:
                                f.write(svg_content)
                            content = json.dumps({'success': True}).encode('utf-8')
                            _scan_cache['data'] = None
                    status = '200 OK'
                    content_type = 'application/json; charset=utf-8'
                else:
                    content = json.dumps({'success': False, 'error': 'Invalid request'}).encode('utf-8')
                    status = '400 Bad Request'
                    content_type = 'application/json; charset=utf-8'
            except Exception as e:
                log('save-svg error: ' + str(e))
                content = json.dumps({'success': False, 'error': str(e)}).encode('utf-8')
                status = '500 Internal Server Error'
                content_type = 'application/json; charset=utf-8'
        
        else:
            content, status, content_type = serve_static_file(path)
    
    except Exception as e:
        log('unhandled error: ' + str(e))
        content = b'<html><body><h1>500 Internal Server Error</h1></body></html>'
        status = '500 Internal Server Error'
        content_type = 'text/html; charset=utf-8'
    
    response_headers = [
        ('Content-Type', content_type),
        ('Cache-Control', 'no-cache, no-store, must-revalidate'),
    ]
    start_response(status, response_headers)
    
    if isinstance(content, str):
        return [content.encode('utf-8')]
    return [content]
'''

def _get_session():
    s = requests.Session()
    s.mount('https://', tls12_adapter)
    s.headers.update(HEADERS)
    return s

def api_request(method, url, max_retries=3, retry_delay=10, **kwargs):
    session = _get_session()
    for attempt in range(max_retries):
        try:
            resp = getattr(session, method)(url, timeout=30, **kwargs)
            return resp
        except requests.exceptions.SSLError as e:
            print(f"    [SSL] 尝试 {attempt+1}/{max_retries} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except requests.exceptions.ConnectionError as e:
            print(f"    [CONN] 尝试 {attempt+1}/{max_retries} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except Exception as e:
            print(f"    [ERR] 尝试 {attempt+1}/{max_retries} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    return None

def git_pull():
    try:
        result = api_request('post', f'https://{HOST}/api/v0/user/{USERNAME}/consoles/', json={'executable': '/bin/bash'})
        if result and result.status_code == 201:
            console_id = result.json()['id']
            print(f"[INFO] 创建控制台: {console_id}")
            
            commands = [
                f'cd /home/ppt/ppt-master && git pull origin main',
            ]
            
            for cmd in commands:
                api_request('post', f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/send_input/', json={'input': cmd + '\\n'})
                print(f"[INFO] 执行: {cmd}")
            
            time.sleep(10)
            
            api_request('delete', f'https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}')
            print("[OK] git pull 完成")
            return True
        else:
            print(f"[!] 无法创建控制台: {result.status_code if result else 'N/A'}")
            return False
    except Exception as e:
        print(f"[!] git pull 失败: {e}")
        return False

def upload_wsgi():
    url = f'https://{HOST}/api/v0/user/{USERNAME}/files/path{WSGI_FILE_PATH}'
    resp = api_request('post', url, files={'content': WSGI_CONTENT}, max_retries=5, retry_delay=15)
    if resp and resp.ok:
        print("[OK] WSGI 上传成功")
        return True
    else:
        print(f"[X] WSGI 上传失败: {resp.status_code if resp else 'Connection failed'}")
        return False

def reload_webapp():
    url = f'https://{HOST}/api/v0/user/{USERNAME}/webapps/{WEBAPP_DOMAIN}/reload/'
    resp = api_request('post', url, max_retries=3, retry_delay=15)
    if resp and resp.ok:
        print("[OK] Web App 重载成功!")
        return True
    else:
        print(f"[X] Web App 重载失败: {resp.status_code if resp else 'Connection failed'}")
        return False

def verify():
    print("\n" + "="*50)
    print("验证网站...")
    print("="*50)

    test_urls = [
        ("首页", "https://ppt.pythonanywhere.com/"),
        ("Viewer", "https://ppt.pythonanywhere.com/viewer.html"),
        ("API", "https://ppt.pythonanywhere.com/api/scan-projects"),
        ("Check", "https://ppt.pythonanywhere.com/api/check-changes"),
    ]

    all_ok = True
    session = _get_session()
    for name, url in test_urls:
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                print(f"[OK] {name}: {response.status_code} ({len(response.text)} bytes)")
            else:
                print(f"[FAIL] {name}: {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            all_ok = False

    return all_ok

def main():
    print("\n" + "#"*50)
    print("# PPT Master Deploy - 部署脚本")
    print("#"*50)

    print("\n[Step 1] 同步代码 (git pull)...")
    git_pull()

    print("\n[Step 2] 上传 WSGI...")
    if not upload_wsgi():
        print("\n[X] WSGI 上传失败")
        sys.exit(1)

    print("\n[Step 3] 重载 Web App...")
    if not reload_webapp():
        print("\n[!] 重载失败，请手动重载")
    else:
        time.sleep(5)

    print("\n[Step 4] 验证网站...")
    verify()

    print("\n" + "#"*50)
    print("# 部署完成!")
    print("#"*50)
    print(f"\n访问: https://ppt.pythonanywhere.com/")
    print(f"Viewer: https://ppt.pythonanywhere.com/viewer.html?project=chongqing-report")

if __name__ == "__main__":
    main()
