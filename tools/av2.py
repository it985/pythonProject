def deduplicate_and_sort(arr):
    # 转为大写并去重
    unique_uppercase = sorted(set(element.upper() for element in arr))
    return unique_uppercase

# 读取av.txt中的数据
with open('av.txt', 'r', encoding='utf-8') as file:
    arr = [line.strip() for line in file]

# 调用去重排序方法
result = deduplicate_and_sort(arr)

# 将结果写入到av2.txt
with open('av2.txt', 'w', encoding='utf-8') as output_file:
    for item in result:
        output_file.write(item + '\n')  # 每个元素写入一行