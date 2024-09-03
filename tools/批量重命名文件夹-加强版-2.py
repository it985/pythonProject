import 重命名

def rename_folders(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            # 允许所有字符，包括标点符号
            new_name = ''.join(e for e in item)
            if item not in ['图文作品', '视频作品'] and new_name:
                new_item_path = os.path.join(directory_path, new_name)
                try:
                    os.rename(item_path, new_item_path)
                    print(f'Renamed "{item}" to "{new_name}"')
                except Exception as e:
                    print(f'Failed to rename "{item}" to "{new_name}". Error: {e}')
            rename_folders(item_path)

if __name__ == '__main__':
    with open('a.txt', 'r', encoding='utf-8') as file:
        for line in file:
            directory_path = line.rstrip()
            if os.path.isdir(directory_path):
                rename_folders(directory_path)
            else:
                print(f'The provided path "{directory_path}" does not exist.')
