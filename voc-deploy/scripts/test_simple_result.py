import requests
import time

time.sleep(5)

print("测试首页...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")
print(f"内容:\n{r.text}")
