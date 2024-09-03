import 重命名

def rename_folders(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            if item in ['图文作品', '视频作品']:
                print(f'Skip renaming "{item}" as it is a special directory')
                rename_folders(item_path)
                continue
            new_name = ''.join(filter(str.isdigit, item))
            new_item_path = os.path.join(directory_path, new_name)
            os.rename(item_path, new_item_path)
            print(f'Renamed "{item}" to "{new_name}"')
            rename_folders(new_item_path)

if __name__ == '__main__':
    directory_path = 'E:\\itheima149\\code\com\\pythonProject\\tools\\1'
    rename_folders(directory_path)
