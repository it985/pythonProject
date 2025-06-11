def filter_unique_elements(a_str, b_str):
    """移除b中包含a元素的Python去重函数"""
    # 将逗号分隔的字符串转换成列表
    list_a = a_str.split(',')
    list_b = b_str.split(',')

    # 创建a的集合用于快速查找
    set_a = set(list_a)
    set_b= set(list_b)

    # 过滤b中不在a里的元素，保留原有顺序
    result = [item for item in list_b if item not in set_a]
    return result


# 测试示例
if __name__ == "__main__":
    input_a = "10673533,11605312,116683,1338715561,1526101,15385187,16539048,2009929,21648772,23400436,250620366,27565758,35579222,3904677,409793037,533996453,632887,7375428,900171,154506630,12473905,154506630,6844293,3314672"
    input_b = ""
    output = filter_unique_elements(input_a, input_b)
    print("过滤后的数组:", output)  # 输出：['789', '890']