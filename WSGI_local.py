import os
import sys
import urllib.parse
import json
import time
import threading
from pathlib import Path

from config import PROJECT_DIR, STATIC_DIR, SCRIPTS_DIR, PROJECT_ALIASES

_file_watch_cache = {}
_last_reload_time = time.time()

SCAN_CACHE_TTL = 60
_scan_cache = {'data': None, 'timestamp': 0}
_cache_lock = threading.Lock()

def _get_valid_cache():
    with _cache_lock:
        if _scan_cache['data'] is None:
            return None
        if time.time() - _scan_cache['timestamp'] > SCAN_CACHE_TTL:
            return None
        return _scan_cache['data']

def _set_cache(data):
    with _cache_lock:
        _scan_cache['data'] = data
        _scan_cache['timestamp'] = time.time()

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

def broadcast_reload(project_id=None, file_path=None):
    global _last_reload_time
    _last_reload_time = time.time()

def invalidate_scan_cache():
    with _cache_lock:
        _scan_cache['data'] = None
        _scan_cache['timestamp'] = 0

def handle_api_path(path, environ, start_response):
    if path == '/api/debug-path':
        content = f"path={path}".encode('utf-8')
        start_response('200 OK', [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))])
        return [content]

    if path == '/api/check-changes':
        changed = scan_project_files()
        if changed:
            invalidate_scan_cache()
        content = json.dumps({'changed': len(changed) > 0, 'files': changed, 'timestamp': _last_reload_time}, ensure_ascii=False).encode('utf-8')
        start_response('200 OK', [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache')])
        return [content]

    if path == '/api/invalidate-cache':
        invalidate_scan_cache()
        content = json.dumps({'success': True, 'message': 'Cache invalidated'}, ensure_ascii=False).encode('utf-8')
        start_response('200 OK', [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache')])
        return [content]

    if path == '/api/scan-projects':
        cached = _get_valid_cache()
        if cached is not None:
            content = cached
        else:
            examples_dir = PROJECT_DIR / 'examples'
            projects = []
            if examples_dir.exists():
                for item in examples_dir.iterdir():
                    if item.is_dir():
                        svg_final = item / 'svg_final'
                        slides = []
                        if svg_final.exists():
                            for svg_file in sorted(svg_final.glob('*.svg')):
                                slides.append({'file': svg_file.name, 'mtime': get_file_mtime(svg_file)})
                        projects.append({
                            'id': item.name,
                            'folder': item.name,
                            'slides': slides,
                            'alias': [k for k, v in PROJECT_ALIASES.items() if v == item.name]
                        })
            content = json.dumps({'projects': projects, 'timestamp': time.time()}, ensure_ascii=False).encode('utf-8')
            _set_cache(content)
        start_response('200 OK', [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache')])
        return [content]

    if path.startswith('/api/export'):
        return handle_export(path, environ, start_response)

    if path == '/api/edit-svg':
        return handle_edit_svg(environ, start_response)

    if path == '/api/save-project':
        return handle_save_project(environ, start_response)

    if path == '/api/projects-data':
        return handle_get_projects_data(start_response)

    return None

def handle_export(path, environ, start_response):
    query = environ.get('QUERY_STRING', '')
    params = urllib.parse.parse_qs(query)
    project_id = params.get('project', [None])[0]

    if not project_id:
        content = b'project parameter required'
        start_response('400 Bad Request', [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))])
        return [content]

    project_folder = get_project_folder(project_id)
    if not project_folder:
        content = f'Project not found: {project_id}'.encode('utf-8')
        start_response('404 Not Found', [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))])
        return [content]

    try:
        if str(SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPTS_DIR))
        from svg_to_pptx import create_pptx_with_native_svg
        import tempfile

        output_dir = Path(tempfile.mkdtemp())
        output_pptx = output_dir / f'{project_id}.pptx'
        svg_files = sorted([f for f in project_folder.glob('*.svg')])

        if not svg_files:
            content = b'No SVG files found'
            start_response('404 Not Found', [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))])
            return [content]

        create_pptx_with_native_svg(svg_files, str(output_pptx), use_native_shapes=True)

        with open(output_pptx, 'rb') as f:
            pptx_content = f.read()

        import shutil
        shutil.rmtree(output_dir)

        response_headers = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
            ('Content-Length', str(len(pptx_content))),
            ('Content-Disposition', f'attachment; filename*=UTF-8\'\'{urllib.parse.quote(project_id)}.pptx')
        ]
        start_response('200 OK', response_headers)
        return [pptx_content]

    except Exception as e:
        import traceback
        content = f'Export failed: {str(e)}\n{traceback.format_exc()}'.encode('utf-8')
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain'), ('Content-Length', str(len(content)))])
        return [content]

def handle_edit_svg(environ, start_response):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
        data = json.loads(request_body)

        file_name = data.get('file')
        folder = data.get('folder')
        old_text = data.get('oldText')
        new_text = data.get('newText')
        element_index = data.get('elementIndex')

        if not all([file_name, folder, old_text is not None, new_text is not None]):
            content = json.dumps({'success': False, 'error': 'Missing required parameters'}).encode('utf-8')
            start_response('400 Bad Request', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
            return [content]

        svg_path = PROJECT_DIR / folder / file_name
        if not svg_path.exists():
            content = json.dumps({'success': False, 'error': f'File not found: {svg_path}'}).encode('utf-8')
            start_response('404 Not Found', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
            return [content]

        backup_path = svg_path.with_suffix('.svg.bak')
        if backup_path.exists():
            backup_path.unlink()
        svg_path.rename(backup_path)

        content_svg = backup_path.read_text(encoding='utf-8')

        if element_index is not None:
            try:
                import xml.etree.ElementTree as ET
                ns = {'svg': 'http://www.w3.org/2000/svg'}
                root = ET.fromstring(content_svg)
                text_elements = root.findall('.//svg:text', ns) or root.findall('.//text')
                idx = int(element_index)
                if 0 <= idx < len(text_elements):
                    text_elem = text_elements[idx]
                    if text_elem.text == old_text:
                        text_elem.text = new_text
                        content_svg = ET.tostring(root, encoding='unicode')
                        if content_svg.startswith('<?xml'):
                            content_svg = content_svg[content_svg.index('?>') + 2:].strip()
                        content_svg = '<?xml version="1.0" encoding="utf-8"?>\n' + content_svg
                    else:
                        backup_path.rename(svg_path)
                        content = json.dumps({'success': False, 'error': 'Text content mismatch'}).encode('utf-8')
                        start_response('400 Bad Request', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
                        return [content]
                else:
                    backup_path.rename(svg_path)
                    content = json.dumps({'success': False, 'error': f'Invalid element index: {idx}'}).encode('utf-8')
                    start_response('400 Bad Request', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
                    return [content]
            except ET.ParseError as e:
                backup_path.rename(svg_path)
                content = json.dumps({'success': False, 'error': f'XML parse error: {str(e)}'}).encode('utf-8')
                start_response('500 Internal Server Error', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
                return [content]
        else:
            content_svg = content_svg.replace(old_text, new_text)

        svg_path.write_text(content_svg, encoding='utf-8')
        invalidate_scan_cache()

        content = json.dumps({'success': True, 'message': 'Text updated successfully'}).encode('utf-8')
        start_response('200 OK', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]

    except json.JSONDecodeError as e:
        content = json.dumps({'success': False, 'error': f'Invalid JSON: {str(e)}'}).encode('utf-8')
        start_response('400 Bad Request', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]
    except Exception as e:
        import traceback
        content = json.dumps({'success': False, 'error': str(e), 'trace': traceback.format_exc()}).encode('utf-8')
        start_response('500 Internal Server Error', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]

def handle_save_project(environ, start_response):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
        data = json.loads(request_body)

        project_id = data.get('id')
        if not project_id:
            content = json.dumps({'success': False, 'error': 'Missing project id'}).encode('utf-8')
            start_response('400 Bad Request', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
            return [content]

        data_file = PROJECT_DIR / 'examples' / 'projects_data.json'
        projects_data = {}
        if data_file.exists():
            projects_data = json.loads(data_file.read_text(encoding='utf-8'))

        projects_data[project_id] = {
            'title': data.get('title'),
            'desc': data.get('desc'),
            'tags': data.get('tags', [])
        }

        data_file.write_text(json.dumps(projects_data, ensure_ascii=False, indent=2), encoding='utf-8')

        content = json.dumps({'success': True, 'message': 'Project saved'}).encode('utf-8')
        start_response('200 OK', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]

    except Exception as e:
        import traceback
        content = json.dumps({'success': False, 'error': str(e), 'trace': traceback.format_exc()}).encode('utf-8')
        start_response('500 Internal Server Error', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]

def handle_get_projects_data(start_response):
    try:
        data_file = PROJECT_DIR / 'examples' / 'projects_data.json'
        if data_file.exists():
            content = data_file.read_text(encoding='utf-8')
        else:
            content = '{}'

        start_response('200 OK', [('Content-Type', 'application/json'), ('Cache-Control', 'no-cache'), ('Content-Length', str(len(content)))])
        return [content.encode('utf-8')]

    except Exception as e:
        content = json.dumps({'error': str(e)}).encode('utf-8')
        start_response('500 Internal Server Error', [('Content-Type', 'application/json'), ('Content-Length', str(len(content)))])
        return [content]

def handle_static_file(path):
    path_clean = path.lstrip('/').split('?')[0]
    path_parts = path_clean.split('/')

    if path_clean in ['viewer.html', 'index.html'] or '/' not in path_clean:
        static_file = STATIC_DIR / path_clean
        if static_file.exists() and static_file.is_file():
            return static_file.read_bytes(), '200 OK'

    if path_clean.startswith('public/'):
        static_file = STATIC_DIR / path_clean.split('/', 1)[1]
        if static_file.exists() and static_file.is_file():
            return static_file.read_bytes(), '200 OK'

    if len(path_parts) >= 2 and path_parts[0] == 'js':
        static_file = STATIC_DIR / path_clean
        if static_file.exists() and static_file.is_file():
            return static_file.read_bytes(), '200 OK'

    return None, None

def handle_examples_file(path):
    path_clean = path.lstrip('/').split('?')[0]
    examples_file = PROJECT_DIR / path_clean

    if not examples_file.exists() or not examples_file.is_file():
        path_parts = path_clean.split('/')
        if len(path_parts) >= 3 and path_parts[0] == 'examples':
            folder_name = path_parts[1]
            resolved = resolve_project_alias(folder_name)

            if resolved == folder_name:
                examples_dir = PROJECT_DIR / 'examples'
                folder = find_best_matching_folder(folder_name, examples_dir)
                if folder:
                    path_parts[1] = folder.name
            else:
                path_parts[1] = resolved

            examples_file = PROJECT_DIR.joinpath(*path_parts)

    if examples_file.exists() and examples_file.is_file():
        return examples_file.read_bytes(), '200 OK', examples_file.suffix

    return None, None, None

def application(environ, start_response):
    global _last_reload_time

    path = environ.get('PATH_INFO', '/')
    path = urllib.parse.unquote(path)
    path = path.encode('latin-1').decode('utf-8', errors='replace')

    api_result = handle_api_path(path, environ, start_response)
    if api_result is not None:
        return api_result

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
        content, status = handle_static_file(path)
        if content:
            content_type = 'text/html; charset=utf-8' if path.endswith('.html') else 'application/octet-stream'
        else:
            content, status, suffix = handle_examples_file(path)
            if content:
                if suffix == '.svg':
                    content_type = 'image/svg+xml; charset=utf-8'
                elif suffix == '.png':
                    content_type = 'image/png'
                else:
                    content_type = 'application/octet-stream'
            else:
                content = f'<html><body><h1>404: {path}</h1></body></html>'.encode('utf-8')
                status = '404 Not Found'
                content_type = 'text/html; charset=utf-8'

    response_headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(content))),
        ('Cache-Control', 'no-cache, no-store, must-revalidate'),
        ('Pragma', 'no-cache'),
        ('Expires', '0')
    ]
    start_response(status, response_headers)
    return [content]
