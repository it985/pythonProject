import json

def remove_duplicates(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    unique_data = list(set(json.dumps(item, sort_keys=True) for item in data))
    unique_data = [json.loads(item) for item in unique_data]

    return unique_data

# 请将'your_file.json'替换为实际的 JSON 文件路径
result = remove_duplicates('1.json')

# 如果需要将去重后的数据写回文件，可以使用以下代码：
with open('1.json', 'w', encoding='utf-8') as file:
    json.dump(result, file)
