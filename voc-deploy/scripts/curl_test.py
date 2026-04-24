import subprocess
import time

time.sleep(3)

print("使用 curl 测试...")

# 测试 SVG
cmd = 'curl -s -o /dev/null -w "%{http_code}" "https://ppt.pythonanywhere.com/examples/ppt169_%E6%88%98%E6%9C%AF%E6%9C%8D%E8%A3%85_%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90/svg_final/P01_%E5%B0%81%E9%9D%A2.svg"'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
print(f"SVG HTTP 状态: {result.stdout}")

# 测试首页
cmd2 = 'curl -s "https://ppt.pythonanywhere.com/" | head -c 500'
result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
print(f"\n首页前 500 字符:")
print(result2.stdout)
