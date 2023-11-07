import os
import subprocess

size_threshold = 5 * 1024 * 1024
file_to_upx = []
for root, dirs, files in os.walk("./build", topdown=False):
    for file in files:
        # 如果是pyd或者dll，且文件大小大于20mb，打印路径
        if (
            (file.endswith(".pyd") or file.endswith(".dll")) or file.endswith(".exe")
        ) and (size := os.path.getsize(os.path.join(root, file))) > size_threshold:
            print(os.path.join(root, file), size)
            file_to_upx.append(os.path.join(root, file))

# 异步执行upx并等待所有upx执行完毕
processes = []
for file in file_to_upx:
    processes.append(subprocess.Popen(["upx", "-9", file, "--force"]))
for process in processes:
    process.wait()
