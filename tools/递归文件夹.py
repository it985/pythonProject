# 递归某一文件夹，若递归到目录名为图文作品或者视频作品，就不在递归，将结果保存到当前目录下的a.txt，用python的main方法
# E:\\1\\dy1\\DY-UP\\主页作品\\
import 重命名

def save_to_file(file_info, filename):
    """将文件信息保存到指定文件"""
    with open(filename, 'a',encoding='utf-8') as file:
        file.write(file_info + '\\n')

def process_directory(directory, exclude_directories):
    """处理目录，不递归到指定的目录名"""
    for entry in os.scandir(directory):
        if entry.is_dir():
            if entry.name not in exclude_directories:
                print(f"Processing directory: {entry.path}")
                process_directory(entry.path, exclude_directories)
            else:
                print(f"Excluding directory: {entry.name}")
        else:
            print(f"Processing file: {entry.path}")

def main():
    """主方法"""
    directory_to_process = r"E:\\1\\dy1\\DY-UP\\主页作品\\"  # 需要处理的目录路径
    exclude_directories = ["图文作品", "视频作品"]  # 不要递归的目录名列表
    result_file = "abackup.txt"  # 结果保存的文件名

    process_directory(directory_to_process, exclude_directories)
    save_to_file("Processing complete.", result_file)

if __name__ == "__main__":
    main()
# import os
#
#
# def save_to_file(file_info, filename):
#     """将文件信息保存到指定文件"""
#     with open(filename, 'a',encoding='utf-8') as file:
#         file.write(file_info + '\\n')
#
#
# def process_directory(directory, exclude_directories, result_file):
#     """处理目录，不递归到指定的目录名，并将结果保存到文件"""
#     for entry in os.scandir(directory):
#         if entry.is_dir():
#             if entry.name not in exclude_directories:
#                 save_to_file(f"Processing directory: {entry.path}", result_file)
#                 process_directory(entry.path, exclude_directories, result_file)
#             else:
#                 save_to_file(f"Excluding directory: {entry.name}", result_file)
#         else:
#             # 这里仅处理目录，不处理文件，如果需要处理文件也可以类似地保存信息
#             pass
#
#
# def main():
#     """主方法"""
#     directory_to_process = r"E:\\1\\dy1\\DY-UP\\主页作品\\"  # 需要处理的目录路径
#     exclude_directories = ["图文作品", "视频作品"]  # 不要递归的目录名列表
#     result_file = "a.txt"  # 结果保存的文件名
#
#     # 初始化结果文件
#     open(result_file, 'w').close()
#
#     process_directory(directory_to_process, exclude_directories, result_file)
#     save_to_file("Processing complete.", result_file)
#
#
# if __name__ == "__main__":
#     main()
