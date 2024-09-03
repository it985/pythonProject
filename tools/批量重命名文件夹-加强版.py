import 重命名

def rename_folders(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            # 递归调用rename_folders处理子目录
            rename_folders(item_path)
            # 对非特定目录进行重命名
            if item not in ['图文作品', '视频作品']:
                new_name = ''.join(filter(str.isdigit, item))
                new_item_path = os.path.join(directory_path, new_name)
                os.rename(item_path, new_item_path)
                print(f'Renamed "{item}" to "{new_name}"')

# # 获取当前工作目录
directory_path = os.getcwd()
# # 调用函数，开始递归重命名
rename_folders(directory_path)

if __name__ == '__main__':
    # 由于已经将directory_path设置为当前目录，以下读取文件部分可以省略
    # 如果需要从文件中读取路径，请取消以下注释
    # with open('a.txt', 'r', encoding='utf-8') as file:
    #     directory_path = file.read().strip()
    # directory_path = directory_path.strip()  # 去除可能的空白字符
    # 确保路径存在
    if os.path.isdir(directory_path):
        rename_folders(directory_path)
    else:
        print(f'The provided path "{directory_path}" does not exist.')
