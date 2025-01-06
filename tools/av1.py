def deduplicate_and_sort(arr):
    # 转为大写并去重
    unique_uppercase = sorted(set(element.upper() for element in arr))
    return unique_uppercase

# 示例数组
arr = [
]

# 调用去重排序方法
result = deduplicate_and_sort(arr)

# 打印去重后的结果
for item in result:
    print(item)
