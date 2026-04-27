import os
import sys
import logging
import time
import threading
from pathlib import Path
from urllib.parse import unquote

from flask import Flask, request, jsonify, send_from_directory, Response

sys.path.insert(0, str(Path(__file__).parent.resolve()))
from config import PROJECT_DIR, STATIC_DIR, SCRIPTS_DIR, PROJECT_ALIASES, PORT

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path='')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('ppt-master')

_file_watch_cache = {}
_last_reload_time = time.time()

USERS = {
    'admin': 'admin',
    'lasen': '123456'
}

TAG_COLORS = {
    'consulting': {'bg': 'rgba(99, 102, 241, 0.2)', 'border': 'rgba(99, 102, 241, 0.5)'},
    'general': {'bg': 'rgba(6, 182, 212, 0.2)', 'border': 'rgba(6, 182, 212, 0.5)'},
    'creative': {'bg': 'rgba(245, 194, 231, 0.2)', 'border': 'rgba(245, 194, 231, 0.5)'}
}

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
    best_match = None
    best_score = -1

    for item in examples_dir.iterdir():
        if not item.is_dir():
            continue
        item_lower = item.name.lower()
        score = 0

        if item_lower == target_lower:
            score = 100
        elif item.name.startswith('ppt169_') and target_name.startswith('ppt169_'):
            target_suffix = target_name[len('ppt169_'):]
            item_suffix = item.name[len('ppt169_'):]
            if target_suffix.split('_')[0] == item_suffix.split('_')[0]:
                score = 50
        elif '顶级咨询风' in target_name and '顶级咨询风' in item.name:
            target_key = target_name.split('_')[2] if len(target_name.split('_')) > 2 else ''
            item_key = item.name.split('_')[2] if len(item.name.split('_')) > 2 else ''
            if target_key and item_key and (target_key in item.name or item.name in target_name):
                score = 30

        if score > best_score:
            best_score = score
            best_match = item

    return best_match

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
    broadcast_reload()

@app.route('/api/debug-path')
def debug_path():
    path = request.path
    return Response(f"path={path}", mimetype='text/plain')

@app.route('/api/check-changes')
def check_changes():
    changed = scan_project_files()
    if changed:
        invalidate_scan_cache()
    return jsonify({
        'changed': len(changed) > 0,
        'files': changed,
        'timestamp': _last_reload_time
    })

@app.route('/api/invalidate-cache', methods=['POST'])
def invalidate_cache():
    invalidate_scan_cache()
    return jsonify({'success': True, 'message': 'Cache invalidated'})

@app.route('/api/scan-projects')
def scan_projects():
    cached = _get_valid_cache()
    if cached is not None:
        return Response(cached, mimetype='application/json')

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

    import json
    content = json.dumps({'projects': projects, 'timestamp': time.time()}, ensure_ascii=False)
    _set_cache(content.encode('utf-8') if isinstance(content, str) else content)
    return Response(content, mimetype='application/json', headers={'Cache-Control': 'no-cache'})

@app.route('/api/projects-data')
def get_projects_data():
    try:
        data_file = PROJECT_DIR / 'examples' / 'projects_data.json'
        if data_file.exists():
            content = data_file.read_text(encoding='utf-8')
        else:
            content = '{}'
        return Response(content, mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    except Exception as e:
        logger.error(f"Error reading projects data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')

        logger.info(f"Login attempt: username={username}")

        if username in USERS and USERS[username] == password:
            return jsonify({'success': True, 'username': username})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})

@app.route('/api/tags', methods=['GET', 'POST'])
def tags():
    try:
        import json
        data_file = PROJECT_DIR / 'examples' / 'tags.json'
        if data_file.exists():
            tags_data = json.loads(data_file.read_text(encoding='utf-8'))
        else:
            tags_data = {'tags': ['consulting', 'general', 'creative']}

        if request.method == 'POST':
            data = request.get_json()
            action = data.get('action')
            if action == 'add':
                new_tag = data.get('tag', '').strip().lower()
                if new_tag and new_tag not in tags_data['tags']:
                    tags_data['tags'].append(new_tag)
                    data_file.write_text(json.dumps(tags_data, ensure_ascii=False, indent=2), encoding='utf-8')
                return jsonify({'success': True, 'tags': tags_data['tags']})
            elif action == 'delete':
                del_tag = data.get('tag', '').strip().lower()
                if del_tag in tags_data['tags']:
                    tags_data['tags'].remove(del_tag)
                    data_file.write_text(json.dumps(tags_data, ensure_ascii=False, indent=2), encoding='utf-8')
                return jsonify({'success': True, 'tags': tags_data['tags']})
            elif action == 'update':
                old_tag = data.get('oldTag', '').strip().lower()
                new_tag = data.get('newTag', '').strip().lower()
                if old_tag in tags_data['tags']:
                    idx = tags_data['tags'].index(old_tag)
                    tags_data['tags'][idx] = new_tag
                    data_file.write_text(json.dumps(tags_data, ensure_ascii=False, indent=2), encoding='utf-8')
                return jsonify({'success': True, 'tags': tags_data['tags']})
            else:
                return jsonify({'success': False, 'error': 'Unknown action'}), 400
        else:
            return jsonify({'success': True, 'tags': tags_data['tags']})
    except Exception as e:
        logger.error(f"Tags error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/edit-svg', methods=['POST'])
def edit_svg():
    try:
        data = request.get_json()
        file_name = data.get('file')
        folder = data.get('folder')
        old_text = data.get('oldText')
        new_text = data.get('newText')
        element_index = data.get('elementIndex')

        if not all([file_name, folder, old_text is not None, new_text is not None]):
            return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

        svg_path = PROJECT_DIR / folder / file_name
        if not svg_path.exists():
            return jsonify({'success': False, 'error': f'File not found: {svg_path}'}), 404

        backup_path = svg_path.with_suffix('.svg.bak')
        if backup_path.exists():
            backup_path.unlink()
        svg_path.rename(backup_path)

        content_svg = backup_path.read_text(encoding='utf-8')

        if element_index is not None:
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
                    return jsonify({'success': False, 'error': 'Text content mismatch'}), 400
            else:
                backup_path.rename(svg_path)
                return jsonify({'success': False, 'error': f'Invalid element index: {idx}'}), 400
        else:
            content_svg = content_svg.replace(old_text, new_text)

        svg_path.write_text(content_svg, encoding='utf-8')
        invalidate_scan_cache()

        return jsonify({'success': True, 'message': 'Text updated successfully'})

    except json.JSONDecodeError as e:
        return jsonify({'success': False, 'error': f'Invalid JSON: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Edit SVG error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save-project', methods=['POST'])
def save_project():
    try:
        import json
        data = request.get_json()
        project_id = data.get('id')
        if not project_id:
            return jsonify({'success': False, 'error': 'Missing project id'}), 400

        data_file = PROJECT_DIR / 'examples' / 'projects_data.json'
        projects_data = {}
        if data_file.exists():
            projects_data = json.loads(data_file.read_text(encoding='utf-8'))

        projects_data[project_id] = {
            'title': data.get('title'),
            'desc': data.get('desc'),
            'style': data.get('style'),
            'tags': data.get('tags', [])
        }

        data_file.write_text(json.dumps(projects_data, ensure_ascii=False, indent=2), encoding='utf-8')
        invalidate_scan_cache()

        return jsonify({'success': True, 'message': 'Project saved'})
    except Exception as e:
        logger.error(f"Save project error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export')
def export():
    project_id = request.args.get('project')
    if not project_id:
        return Response('project parameter required', mimetype='text/plain', status=400)

    project_folder = get_project_folder(project_id)
    if not project_folder:
        return Response(f'Project not found: {project_id}', mimetype='text/plain', status=404)

    try:
        if str(SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPTS_DIR))
        from svg_to_pptx import create_pptx_with_native_svg
        import tempfile
        from urllib.parse import quote

        output_dir = Path(tempfile.mkdtemp())
        output_pptx = output_dir / f'{project_id}.pptx'
        svg_files = sorted([f for f in project_folder.glob('*.svg')])

        if not svg_files:
            return Response('No SVG files found', mimetype='text/plain', status=404)

        create_pptx_with_native_svg(svg_files, str(output_pptx), use_native_shapes=True)

        with open(output_pptx, 'rb') as f:
            pptx_content = f.read()

        import shutil
        shutil.rmtree(output_dir)

        response = Response(
            pptx_content,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(project_id)}.pptx"
        return response

    except Exception as e:
        import traceback
        logger.error(f"Export failed: {e}\n{traceback.format_exc()}")
        return Response(f'Export failed: {str(e)}', mimetype='text/plain', status=500)

@app.route('/')
def index():
    index_file = STATIC_DIR / 'index.html'
    if index_file.exists():
        return send_from_directory(STATIC_DIR, 'index.html')
    return '<html><body><h1>index.html not found</h1></body></html>', 404

@app.route('/viewer.html')
def viewer():
    viewer_file = STATIC_DIR / 'viewer.html'
    if viewer_file.exists():
        return send_from_directory(STATIC_DIR, 'viewer.html')
    return '<html><body><h1>viewer.html not found</h1></body></html>', 404

@app.route('/examples/<path:filename>')
def serve_examples(filename):
    filename = unquote(filename)
    path_parts = filename.split('/')

    if len(path_parts) >= 2:
        folder_name = path_parts[0]
        resolved = resolve_project_alias(folder_name)
        if resolved != folder_name:
            path_parts[0] = resolved

    if len(path_parts) >= 2:
        examples_file = PROJECT_DIR / 'examples' / path_parts[0] / '/'.join(path_parts[1:])
    else:
        examples_file = PROJECT_DIR / 'examples' / filename

    if examples_file.exists() and examples_file.is_file():
        suffix = examples_file.suffix
        if suffix == '.svg':
            mimetype = 'image/svg+xml; charset=utf-8'
        elif suffix == '.png':
            mimetype = 'image/png'
        else:
            mimetype = 'application/octet-stream'
        return send_from_directory(examples_file.parent, examples_file.name, mimetype=mimetype)

    return '<html><body><h1>404: {}</h1></body></html>'.format(filename), 404

if __name__ == '__main__':
    logger.info(f"Starting PPT Master server on port {PORT}")
    logger.info(f"Access: http://localhost:{PORT}/viewer.html")
    app.run(host='localhost', port=PORT, debug=False, threaded=True)