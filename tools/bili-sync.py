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
    input_a = "10673533,11473818,11605312,116683,12473905,1323218982,1338715561,1526101,15385187,154506630,1600113,16539048,16668448,18841842,2009929,21648772,2223018,23400436,250620366,26177922,2691287,27565758,31955376,3314672,354962346,35579222,3904677,409793037,49676,5128039,533996453,632887,6844293,7375428,900171"
    input_b = ""
    output = filter_unique_elements(input_a, input_b)
    print("过滤后的数组:", output)  # 输出：['789', '890']