import requests
import time

time.sleep(3)

try:
    r = requests.get('https://ppt.pythonanywhere.com/trace', timeout=30)
    print(r.text)
except Exception as e:
    print(f"错误: {e}")
