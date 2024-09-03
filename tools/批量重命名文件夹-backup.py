# E:\\itheima149\\code\com\\pythonProject\\tools\\1
# 我有多个目录夹，目录夹名的规律是数字+其他组合而成，
# 比如
# 文件夹一：73254477701128717181我期待雪和有你的冬天
# 文件夹二：73227022791386104701#随拍，
# 文件夹三：73239759355925169021有穿裤子的哦！
# 现在要求写个python将原来文件夹名改成纯数字，如以下
# 文件夹一：73254477701128717181我期待雪和有你的冬天
# 文件夹二：73227022791386104701#随拍，
# 文件夹三：73239759355925169021有穿裤子的哦！
import 重命名

def rename_folders(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            if item in ['图文作品', '视频作品']:
                print(f'Skip renaming "{item}" as it is a special directory')
                rename_folders(item_path)  # 继续递归处理子目录
                continue
            new_name = ''.join(filter(str.isdigit, item))
            new_item_path = os.path.join(directory_path, new_name)
            os.rename(item_path, new_item_path)
            print(f'Renamed "{item}" to "{new_name}"')
            rename_folders(new_item_path)  # 递归调用处理子文件夹

if __name__ == '__main__':
    # 指定需要遍历的目录
    directory_path = 'E:\\itheima149\\code\com\\pythonProject\\tools\\1'
    # directory_path = 'E:\\itheima149\\code\com\\pythonProject\\tools\\1'
    # 调用函数，开始重命名文件夹
    rename_folders(directory_path)
# 修改代码，若目录名为图文作品或者视频作品也会继续运行


# 当前文件夹
# import os
#
# def rename_folders(directory_path):
#     for item in os.listdir(directory_path):
#         item_path = os.path.join(directory_path, item)
#         if os.path.isdir(item_path):
#             new_name = ''.join(filter(str.isdigit, item))
#             new_item_path = os.path.join(directory_path, new_name)
#             os.rename(item_path, new_item_path)
#             print(f'Renamed "{item}" to "{new_name}"')
#             rename_folders(new_item_path)  # 递归调用处理子文件夹
#
# if __name__ == '__main__':
#     # 获取当前目录
#     directory_path = os.getcwd()
#     # 调用函数，开始重命名文件夹
#     rename_folders(directory_path)
