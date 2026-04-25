import os
import sys
import time
import traceback
from pathlib import Path

LOG_FILE = Path(__file__).parent / 'server.log'

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def main():
    log("Starting backend server...")

    try:
        from wsgiref.simple_server import make_server
        from WSGI_local import application

        log("WSGI app imported successfully")

        srv = make_server('localhost', 5001, application)
        log("Server created on port 5001")

        log("Server ready! Accepting connections...")
        srv.serve_forever()

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
