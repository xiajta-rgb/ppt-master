#!/usr/bin/env python
import sys
import socket
import subprocess
import time
import signal
import os
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

def start_backend():
    if is_server_running():
        print(f"[WARN] Backend already running on port {PORT}")
        return None

    pid = find_process_on_port(PORT)
    if pid:
        print(f"[INFO] Found process {pid} on port {PORT}, terminating...")
        kill_process(pid)
        time.sleep(1)

    print(f"[INFO] Starting Flask backend on port {PORT}...")

    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'app'],
            cwd=str(PROJECT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        PID_FILE.write_text(str(process.pid))

        time.sleep(2)

        if is_server_running():
            actual_pid = find_process_on_port(PORT)
            print(f"[OK] Backend started successfully (PID: {process.pid}, Actual: {actual_pid})")
            return process
        else:
            print("[ERROR] Backend failed to start")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to start backend: {e}")
        return None

def stop_server():
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
            print(f"[OK] Killed process {pid}")
        except:
            pass
        PID_FILE.unlink()

    pid = find_process_on_port(PORT)
    if pid:
        print(f"[INFO] Stopping server (PID: {pid})...")
        kill_process(pid)
    else:
        print("[WARN] No server running")

    if PID_FILE.exists():
        PID_FILE.unlink()
    print("[OK] Server stopped")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        stop_server()
    else:
        stop_server()
        start_backend()
        print(f"[INFO] Access: http://localhost:{PORT}/viewer.html")
        print("[INFO] Press Ctrl+C to stop the server")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down...")
            stop_server()