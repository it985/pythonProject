# 写一个python脚本，批量在前面加deny
# 定义输入和输出文件名
input_file = 'ip_list.txt'  # 输入文件名
output_file = 'blacklist.conf'  # 输出文件名

# 打开输入文件并读取内容
with open(input_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# 打开输出文件准备写入
with open(output_file, 'w', encoding='utf-8') as outfile:
    for line in lines:
        # 去掉行末的换行符并添加 'deny'
        outfile.write(f"deny {line.strip()};\n")

print(f"处理完成，结果已写入 {output_file}")
