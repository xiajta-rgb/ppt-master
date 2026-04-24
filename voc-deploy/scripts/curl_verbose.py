import subprocess

print("详细检查请求...")

# 完整输出
cmd = 'curl -v "https://ppt.pythonanywhere.com/" 2>&1'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
print(result.stdout[:2000])
