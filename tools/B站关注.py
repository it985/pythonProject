import json
import os

# 读取 JSON 数据的文件路径
input_file = 'export_uids.json'

# 创建目录以保存生成的 JSON 文件
output_dir = 'tag_json_files'
os.makedirs(output_dir, exist_ok=True)

# 从文件读取数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 按 tag 分组数据
tag_dict = {}

for entry in data:
    for tag in entry['tag']:
        if tag not in tag_dict:
            tag_dict[tag] = []
        tag_dict[tag].append(entry)

# 为每个 tag 创建 JSON 文件
for tag, entries in tag_dict.items():
    file_path = os.path.join(output_dir, f"{tag}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

print(f"生成了 {len(tag_dict)} 个 JSON 文件，存储在 '{output_dir}' 目录中。")
