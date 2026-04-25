#!/usr/bin/env python
import sys
import socket
import subprocess
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).parents[3].resolve()
sys.path.insert(0, str(PROJECT_DIR))
from config import PORT

PID_FILE = PROJECT_DIR / '.server_pid'

def find_process_on_port(port):
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if f':{port}' in part and i > 0:
                        pid = parts[-1]
                        return int(pid)
        return None
    except Exception as e:
        print(f"[WARN] Failed to check port: {e}")
        return None

def kill_process(pid):
    try:
        subprocess.run(['taskkill', '/PID', str(pid), '/F'])
        print(f"[OK] Killed process {pid}")
        return True
    except Exception as e:
        print(f"[WARN] Failed to kill process {pid}: {e}")
        return False

def is_server_running():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', PORT))
        sock.close()
        return result == 0
    except:
        return False

def start_server():
    if is_server_running():
        print(f"[WARN] Server already running on port {PORT}")
        return False

    pid = find_process_on_port(PORT)
    if pid:
        print(f"[INFO] Found process {pid}占用端口 {PORT}, terminating...")
        kill_process(pid)
        time.sleep(1)

    print(f"[INFO] 启动服务器 on port {PORT}...")
    print(f"[INFO] 访问地址: http://localhost:{PORT}/viewer.html")

    script = 'from wsgiref.simple_server import make_server; from WSGI_local import application; srv = make_server("localhost", 5001, application); srv.serve_forever()'

    try:
        process = subprocess.Popen(
            [sys.executable, '-c', script],
            cwd=str(PROJECT_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

        PID_FILE.write_text(str(process.pid))

        time.sleep(1)

        if is_server_running():
            actual_pid = find_process_on_port(PORT)
            print(f"[OK] 服务器启动成功 (PID: {actual_pid})")
            print(f"[INFO] 访问 http://localhost:{PORT}/viewer.html")
            print(f"[INFO] 按 Ctrl+C 停止服务器，或运行: python start_server.py stop")
        else:
            print("[ERROR] 服务器启动失败")
            return False

    except Exception as e:
        print(f"[ERROR] 启动失败: {e}")
        return False

    return True

def stop_server():
    pid = find_process_on_port(PORT)
    if pid:
        print(f"[INFO] Stopping server (PID: {pid})...")
        kill_process(pid)
        if PID_FILE.exists():
            PID_FILE.unlink()
        print("[OK] Server stopped")
    else:
        print("[WARN] No server running")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        stop_server()
    else:
        start_server()
