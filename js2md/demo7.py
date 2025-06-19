import json
import os

json_folder = 'chinese-poetry-master/'  # 指定包含JSON文件的文件夹路径
# 遍历文件夹及其子文件夹
for root, dirs, files in os.walk(json_folder):
    # 遍历每个文件
    for file in files:
        # 检查文件扩展名是否为JSON
        if file.endswith('.json'):
            json_path = os.path.join(root, file)  # 构建JSON文件的完整路径
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 创建Markdown文本
            markdown_text = ""
            for dictionary in data:
                markdown_text += f"# {dictionary['title']}\n\n"
                markdown_text += f"**作者：{dictionary['author']}**\n\n"
                markdown_text += f"**韵律：{dictionary['rhythmic']}**\n\n"
                markdown_text += "## 译文\n\n"
                for paragraph in dictionary['paragraphs']:
                    markdown_text += f"{paragraph}\n\n"
                markdown_text += "## 注释\n\n"
                for note in dictionary['notes']:
                    markdown_text += f"- {note}\n"
            output_file = os.path.splitext(json_path)[0] + ".md"  # 生成Markdown文件名
            os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 确保输出文件夹存在
            # 将Markdown文本保存到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_text)