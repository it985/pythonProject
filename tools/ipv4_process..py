# def replace_last_octet_with_zero(ip):
#     # 将IP地址分割成四个部分
#     octets = ip.strip().split('.')
#     # 将第四个字节替换为0
#     octets[3] = '0'
#     # 将修改后的IP地址重新组合，并添加'/24'
#     return '.'.join(octets) + '/24'
# def process_ipv4_file(input_file, output_file):
#     # 打开输入文件并读取内容
#     with open(input_file, 'r', encoding='utf-8') as infile:
#         lines = infile.readlines()
#     # 处理文件内容，去除每行的换行符，然后处理IP地址，最后添加换行符
#     processed_lines = [replace_last_octet_with_zero(line.strip()) + '\n' for line in lines]
#     # 将处理后的内容写入新的文件
#     with open(output_file, 'w', encoding='utf-8') as outfile:
#         outfile.writelines(processed_lines)
# def main():
#     # 定义输入和输出文件名
#     input_file = 'a1.txt'
#     output_file = 'processed_a.txt'
#     # 处理IPv4文件
#     process_ipv4_file(input_file, output_file)
# if __name__ == '__main__':
#     main()

def replace_last_octet_with_zero(ip):
    # 将IP地址分割成四个部分
    octets = ip.strip().split('.')
    # 检查第四个字节是否已经是0/24
    if octets[3] == '0/24':
        return ip  # 如果是，则直接返回原IP地址
    # 将第四个字节替换为0
    octets[3] = '0'
    # 将修改后的IP地址重新组合，并添加'/24'
    return '.'.join(octets) + '/24'

def process_ipv4_file(input_file, output_file):
    # 打开输入文件并读取内容
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    # 处理文件内容，去除每行的换行符，然后处理IP地址，最后添加换行符
    processed_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith('0/24'):
            processed_lines.append(stripped_line)  # 如果已经是0/24，则跳过
        else:
            processed_lines.append(replace_last_octet_with_zero(stripped_line) + '\n')
    # 将处理后的内容写入新的文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(processed_lines)

def main():
    # 定义输入和输出文件名
    input_file = 'a1.txt'
    output_file = 'processed_a.txt'
    # 处理IPv4文件
    process_ipv4_file(input_file, output_file)

if __name__ == '__main__':
    main()
