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
        from WSGI_local import application
        from waitress import serve

        log("WSGI app imported successfully")

        log("Server ready! Accepting connections on port 5001...")
        serve(application, host='localhost', port=5001)

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
