def deduplicate_and_sort(arr):
    # 只去重不转为大写
    unique_elements = sorted(set(arr))
    # random.shuffle(unique_elements) #随机
    return unique_elements

# 读取dy.txt中的数据
with open('dy.txt', 'r', encoding='utf-8') as file:
    arr = [line.strip() for line in file]

# 调用去重排序方法
result = deduplicate_and_sort(arr)

# 将结果写入到dy2.txt
with open('dy2.txt', 'w', encoding='utf-8') as output_file:
    for item in result:
        output_file.write(item + '\n')  # 每个元素写入一行