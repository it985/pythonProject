import sys

# 初始化最小时间为一个很大的数
min_time = sys.maxsize
best_combination = None

# 穷举 x, y, a, b, c
for x in range(1, 4):  # x 从 1 到 3
    for y in range(1, 4):  # y 从 1 到 3
        for a in range(11, 101):  # a 从 11 到 100
            for b in range(11, 101):  # b 从 11 到 100
                for c in range(11, 101):  # c 从 11 到 100
                    total_time = 1646 * (x * a + c) + 20 * (y * b)
                    if total_time < min_time:
                        min_time = total_time
                        best_combination = (x, y, a, b, c)

# 将总时间转换为小时
min_time_minutes = min_time / 60 / 60

# 输出结果
print("最小总休息时间（小时）:", min_time_minutes)
print("最佳组合 (x, y, a, b, c):", best_combination)
