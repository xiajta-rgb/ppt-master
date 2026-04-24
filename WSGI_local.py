import os
import sys
import urllib.parse
import json
import time
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r'c:\Users\xiajt\Documents\trae_projects\ppt-master')
STATIC_DIR = PROJECT_DIR / 'public'

SCRIPTS_DIR = PROJECT_DIR / '.trae' / 'skills' / 'ppt-master' / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

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
}

_file_watch_cache = {}
_last_reload_time = time.time()
_sse_clients = []

def resolve_project_alias(project_id):
    if project_id in PROJECT_ALIASES:
        return PROJECT_ALIASES[project_id]
    return project_id

def find_best_matching_folder(target_name, examples_dir):
    target_lower = target_name.lower()

    for item in examples_dir.iterdir():
        if not item.is_dir():
            continue
        name_lower = item.name.lower()

        if name_lower == target_lower:
            return item

    prefix = 'ppt169_'
    if target_name.startswith(prefix):
        suffix = target_name[len(prefix):]
        for item in examples_dir.iterdir():
            if not item.is_dir():
                continue
            if item.name.startswith(prefix) and suffix.split('_')[0] in item.name:
                return item

    for item in examples_dir.iterdir():
        if not item.is_dir():
            continue
        name_lower = item.name.lower()
        if '顶级咨询风' in target_name and '顶级咨询风' in item.name:
            key1 = target_name.split('_')[2] if len(target_name.split('_')) > 2 else ''
            key2 = item.name.split('_')[2] if len(item.name.split('_')) > 2 else ''
            if key1 and key2 and (key1 in item.name or item.name in target_name):
                return item

    return None

def get_project_folder(project_id):
    resolved_id = resolve_project_alias(project_id)
    examples_dir = PROJECT_DIR / 'examples'
    if examples_dir.exists():
        folder = find_best_matching_folder(resolved_id, examples_dir)
        if folder:
            svg_final = folder / 'svg_final'
            if svg_final.exists():
                return svg_final
    return None

def get_file_mtime(file_path):
    try:
        return os.path.getmtime(file_path)
    except:
        return 0

def scan_project_files():
    global _file_watch_cache
    examples_dir = PROJECT_DIR / 'examples'
    current_files = {}

    if examples_dir.exists():
        for project_dir in examples_dir.iterdir():
            if project_dir.is_dir():
                svg_final = project_dir / 'svg_final'
                if svg_final.exists():
                    for svg_file in svg_final.glob('*.svg'):
                        key = str(svg_file.relative_to(PROJECT_DIR))
                        current_files[key] = get_file_mtime(svg_file)

    changed_files = []
    for file_path, mtime in current_files.items():
        if file_path not in _file_watch_cache or _file_watch_cache[file_path] != mtime:
            changed_files.append(file_path)

    _file_watch_cache = current_files
    return changed_files

def notify_sse_clients(event_type, data):
    message = f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
    for client in _sse_clients[:]:
        try:
            client(message.encode('utf-8'))
        except:
            _sse_clients.remove(client)

def broadcast_reload(project_id=None, file_path=None):
    global _last_reload_time
    _last_reload_time = time.time()
    notify_sse_clients('reload', {
        'timestamp': _last_reload_time,
        'project': project_id,
        'file': file_path
    })

class SSECLient:
    def __init__(self, start_response):
        self.start_response = start_response
        self.closed = False

    def __call__(self, data):
        if not self.closed:
            try:
                self.start_response('200 OK', [('Content-Type', 'text/event-stream'),
                                                ('Cache-Control', 'no-cache'),
                                                ('Connection', 'keep-alive')])
            except:
                pass

    def close(self):
        self.closed = True
        if self in _sse_clients:
            _sse_clients.remove(self)

def application(environ, start_response):
    global _last_reload_time

    path = environ.get('PATH_INFO', '/')

    if '%' in path:
        try:
            path = urllib.parse.unquote(path)
        except:
            pass

    print(f"[DEBUG] PATH_INFO received: {path}")

    if path == '/api/debug-path':
        content = f"path={path}".encode('utf-8')
        response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))]
        start_response('200 OK', response_headers)
        return [content]

    if path == '/api/events':
        client = SSECLient(start_response)
        _sse_clients.append(client)
        changed_files = scan_project_files()
        if changed_files:
            client(f"data: {json.dumps({'type': 'initial', 'files': changed_files}, ensure_ascii=False)}\n\n".encode('utf-8'))
        return []

    if path == '/api/check-changes':
        changed = scan_project_files()
        status = '200 OK'
        content = json.dumps({'changed': len(changed) > 0, 'files': changed, 'timestamp': _last_reload_time}, ensure_ascii=False).encode('utf-8')
        response_headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache')]
        start_response(status, response_headers)
        return [content]

    if path == '/api/scan-projects':
        examples_dir = PROJECT_DIR / 'examples'
        projects = []
        if examples_dir.exists():
            for item in examples_dir.iterdir():
                if item.is_dir():
                    svg_final = item / 'svg_final'
                    slides = []
                    if svg_final.exists():
                        for svg_file in sorted(svg_final.glob('*.svg')):
                            slides.append({
                                'file': svg_file.name,
                                'mtime': get_file_mtime(svg_file)
                            })
                    projects.append({
                        'id': item.name,
                        'folder': item.name,
                        'slides': slides,
                        'alias': [k for k, v in PROJECT_ALIASES.items() if v == item.name]
                    })
        status = '200 OK'
        content = json.dumps({'projects': projects, 'timestamp': time.time()}, ensure_ascii=False).encode('utf-8')
        response_headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache')]
        start_response(status, response_headers)
        return [content]

    if path.startswith('/api/export'):
        project_id = None
        query = environ.get('QUERY_STRING', '')
        params = urllib.parse.parse_qs(query)
        if 'project' in params:
            project_id = params['project'][0]

        if not project_id:
            status = '400 Bad Request'
            content = b'project parameter required'
            response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))]
            start_response(status, response_headers)
            return [content]

        project_folder = get_project_folder(project_id)

        if not project_folder:
            status = '404 Not Found'
            content = f'Project not found: {project_id}'.encode('utf-8')
            response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))]
            start_response(status, response_headers)
            return [content]

        try:
            from svg_to_pptx import create_pptx_with_native_svg
            import tempfile

            output_dir = Path(tempfile.mkdtemp())
            output_pptx = output_dir / f'{project_id}.pptx'

            svg_files = sorted([f for f in project_folder.glob('*.svg')])
            if not svg_files:
                status = '404 Not Found'
                content = b'No SVG files found'
                response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))]
                start_response(status, response_headers)
                return [content]

            create_pptx_with_native_svg(svg_files, str(output_pptx), use_native_shapes=True)

            with open(output_pptx, 'rb') as f:
                pptx_content = f.read()

            import shutil
            shutil.rmtree(output_dir)

            status = '200 OK'
            response_headers = [
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
                ('Content-Length', str(len(pptx_content))),
                ('Content-Disposition', f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(project_id)}.pptx')
            ]
            start_response(status, response_headers)
            return [pptx_content]

        except Exception as e:
            import traceback
            status = '500 Internal Server Error'
            content = f'Export failed: {str(e)}\n{traceback.format_exc()}'.encode('utf-8')
            response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))]
            start_response(status, response_headers)
            return [content]

    if path == '/' or path == '':
        index_file = STATIC_DIR / 'index.html'
        if index_file.exists():
            content = index_file.read_bytes()
            status = '200 OK'
            content_type = 'text/html; charset=utf-8'
        else:
            content = b'<html><body><h1>index.html not found</h1></body></html>'
            status = '404 Not Found'
            content_type = 'text/html; charset=utf-8'
    else:
            path_clean = path.lstrip('/')
            examples_file = PROJECT_DIR / path_clean
            if not examples_file.exists() or not examples_file.is_file():
                path_parts = path_clean.split('/')
                if len(path_parts) >= 3 and path_parts[0] == 'examples':
                    folder_name = path_parts[1]
                    resolved = resolve_project_alias(folder_name)
                    print(f"[DEBUG] folder_name={folder_name}, resolved={resolved}")
                    if resolved == folder_name:
                        examples_dir = PROJECT_DIR / 'examples'
                        folder = find_best_matching_folder(folder_name, examples_dir)
                        print(f"[DEBUG] find_best_matching_folder({folder_name}) = {folder}")
                        if folder:
                            path_parts[1] = folder.name
                    else:
                        path_parts[1] = resolved
                    examples_file = Path(*path_parts)
                    print(f"[DEBUG] final path_parts={path_parts}, exists={examples_file.exists()}")
            if examples_file.exists() and examples_file.is_file():
                content = examples_file.read_bytes()
                status = '200 OK'
                if examples_file.suffix == '.svg':
                    content_type = 'image/svg+xml; charset=utf-8'
                elif examples_file.suffix == '.png':
                    content_type = 'image/png'
                else:
                    content_type = 'application/octet-stream'
            else:
                content = f'<html><body><h1>404: {path}</h1></body></html>'.encode('utf-8')
                status = '404 Not Found'
                content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content]