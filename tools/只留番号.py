import re


def process_text(text):
    lines = text.strip().split('\n')
    results = []
    original_count = len(lines)
    processed_count = 0

    for line in lines:
        if not line.strip():  # 跳过空行
            continue

        # 找到第一个字母的位置
        match_letter = re.search(r'[A-Za-z]', line)
        if match_letter:
            # 从第一个字母开始截取
            line = line[match_letter.start():]

            # 找到字母-数字模式，使用更宽松的正则表达式
            match_pattern = re.search(r'([A-Za-z]+-\d+)', line)
            if match_pattern:
                results.append(match_pattern.group(1))
                processed_count += 1
            else:
                # 如果没有找到标准模式，尝试更宽松的匹配
                # 查找任何字母序列后跟连字符和数字序列
                alt_match = re.search(r'([A-Za-z]+[\-_]\d+)', line)
                if alt_match:
                    results.append(alt_match.group(1))
                    processed_count += 1
                else:
                    print(f"警告: 无法处理行: {line}")
        else:
            print(f"警告: 未找到字母: {line}")

    print(f"原始数据: {original_count}行, 处理后: {processed_count}行")
    if original_count != processed_count:
        print(f"丢失了 {original_count - processed_count} 行数据")

    return results


# 测试代码
if __name__ == "__main__":
    # 从文件读取数据，如果有文件的话
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        # 示例数据
        text = """


"""

    processed_results = process_text(text)

    # 输出结果
    print("\n处理结果:")
    for result in processed_results:
        print(result)

    # 保存结果到文件
    with open("results.txt", "w", encoding="utf-8") as f:
        for result in processed_results:
            f.write(f"{result}\n")

    print(f"\n结果已保存到 results.txt，共 {len(processed_results)} 条记录")