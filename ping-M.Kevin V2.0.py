# 添加 M.Kevin 的文本 logo
logo = r"""                              
     ____________             _    _
    |____________|           | |  / /
   /  /  | |   \ \           | |/ /
  /  /   | |    \ \          | |\ \ 
 /  /    | |     \ \    _    | |  \ \ 
/__/     |_|      \ \  |_|   |_|    \_\ 
"""

import os
import concurrent.futures
import subprocess
import time

def extract_ip(value):
    """从 value 中提取 ip 地址"""
    # 如果 value 以 http:// 或 https:// 开头，则去掉
    value = value.lstrip("http://").lstrip("https://")

    # 提取 IP 地址（假设 IP 地址是以 : 分隔的第一个字段）
    ip_address = value.strip().split(':')[0]

    return ip_address

def read_file(file_path):
    """读取 txt 文件，生成字典，其中 key 为 id，value 为每行信息"""
    data_dict = {}
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=1):
            # 提取行中的 IP 地址
            ip_address = extract_ip(line)
            data_dict[idx] = ip_address
    return data_dict

def ping_and_save(data_dict, key, value, file_folder):
    """执行 ping 命令，并保存结果到文件"""
    # 构建 ping 命令
    command = ["ping", value]

    try:
        # 使用 subprocess.PIPE 获取命令的标准输出
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)

        # 打印命令的标准输出
        print(result.stdout)

        # 如果命令成功执行且有响应，将 id 和 value 添加到结果字典中
        with open(os.path.join(file_folder, "result.txt"), 'a') as file:
            file.write(f"{key}: {value}\n")
    except subprocess.CalledProcessError as e:
        # 如果 ping 失败，打印错误信息
        print(e.stderr)

def scan(data_dict, interval, file_folder):
    """对字典中的 id 对应的 value 进行 ping 命令"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for key, value in data_dict.items():
            # 提交任务到线程池，每个任务对应一个 ping 命令
            future = executor.submit(ping_and_save, data_dict, key, value, file_folder)
            futures.append(future)

            # 间隔一段时间再提交下一个 ping
            time.sleep(interval)

        # 等待所有任务完成
        concurrent.futures.wait(futures)

# 显示 M.Kevin 的文本 logo
print(logo)

# 选择 txt 文件
file_path = input("请输入 txt 文件路径: ")

# 调用 read_file 函数并接收返回值
data_dict = read_file(file_path)

# 获取文件夹路径
file_folder = os.path.dirname(file_path)

# 定义时间间隔
interval = int(input("请输入 ping 命令的时间间隔（秒）: "))

# 进行 ping 命令
scan(data_dict, interval, file_folder)
print(f"结果已保存到 {os.path.join(file_folder, 'result.txt')}")