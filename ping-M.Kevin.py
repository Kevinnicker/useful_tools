logo = r"""                              
     ____________             _    _
    |____________|           | |  / /
   /  /  | |   \ \           | |/ /
  /  /   | |    \ \          | |\ \ 
 /  /    | |     \ \    _    | |  \ \ 
/__/     |_|      \ \  |_|   |_|    \_\ 
"""

import os
import subprocess
import time

def read_file(file_path):
    """读取txt文件，生成字典，其中key为id，value为每行信息"""
    data_dict = {}
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=1):
            # 提取行中的 IP 地址（假设 IP 地址是行中的第一个字段）
            ip_address = line.strip().split(':')[0]
            data_dict[idx] = ip_address
    return data_dict

def scan(data_dict, interval):
    """对字典中的id对应的value进行ping命令"""
    result_dict = {}
    for key, value in data_dict.items():
        # 构建ping命令
        command = ["ping", value]

        # 执行ping命令
        try:
            # 使用subprocess.check_output获取命令的输出
            subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)

            # 如果命令成功执行且有响应，将id和value添加到结果字典中
            result_dict[key] = value
        except subprocess.CalledProcessError:
            pass  # 如果ping失败，继续下一个id

        # 间隔一段时间再进行下一个ping
        time.sleep(interval)

    return result_dict

def save_to_file(result_dict, file_folder):
    """将ping成功的id和对应的value保存到文件"""
    output_file = os.path.join(file_folder, "result.txt")
    with open(output_file, 'w') as file:
        for key, value in result_dict.items():
            file.write(f"{key}: {value}\n")
    return output_file

def main():
    # 显示 logo
    print(logo)
    # 选择txt文件
    file_path = input("请输入txt文件路径: ")

    # 获取文件夹路径
    file_folder = os.path.dirname(file_path)

    # 读取文件生成字典
    data_dict = read_file(file_path)

    # 定义时间间隔
    interval = int(input("请输入ping命令的时间间隔（秒）: "))

    # 进行ping命令
    result_dict = scan(data_dict, interval)

    # 保存ping成功的结果到文件
    output_file = save_to_file(result_dict, file_folder)
    print(f"结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
