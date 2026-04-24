import requests
import time

time.sleep(8)

print("测试 https://ppt.pythonanywhere.com/ ...")
r = requests.get('https://ppt.pythonanywhere.com/', timeout=30)
print(f"状态: {r.status_code}")
print(f"长度: {len(r.text)}")

if 'renderProjects()' in r.text:
    print("[OK] 包含 renderProjects()")
    print("\n项目列表应该可以正常显示了！")
else:
    print("[X] 不包含 renderProjects()")

# 测试静态文件
r2 = requests.get('https://ppt.pythonanywhere.com/index.html', timeout=30)
print(f"\n/index.html 状态: {r2.status_code}")
