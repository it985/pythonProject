import random
from collections import deque


def magic():
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    # print(f"最初的的13张牌：{cards}")
    random.shuffle(cards)
    # print(f"打乱顺序的13张牌：{cards}")

    # 随机选择4张牌
    random_4_cards = random.sample(cards, 4)
    # print(f"随机抽出的4张牌：{random_4_cards}")
    # 对折后撕开得到8张牌
    random_8_cards = deque(random_4_cards * 2)
    # print(f"对折后撕开得到8张牌：{random_8_cards}")

    # 1. 根据名字有几个字，将前几张牌移到最后
    name = int(random.randint(1, 10))
    # 将双端队列中的元素向左旋转几个位置
    random_8_cards.rotate(-name)
    # print(f"根据名字字数调整后的牌：{random_8_cards}")

    # 2. 取出前三张牌并随机插入剩余牌中，不能插在第一张和最后一张
    first_three = [random_8_cards.popleft() for _ in range(3)]
    # print(f"上面3张牌是：{first_three}")
    # print(f"下面5张牌是：{random_8_cards}")

    for card in first_three:
        insert_position = random.randint(1, len(random_8_cards) - 2)
        random_8_cards.insert(insert_position, card)
    #     print(f"插入牌是：{card}，随机插入位置是：{insert_position + 1}，新牌顺序是{random_8_cards}")
    # print(f"上面3张牌随机插入剩下牌中间，此时新牌顺序：{random_8_cards}")

    # 3. 把最上面的牌藏起来
    remembered_card = random_8_cards.popleft()
    # print(f"藏起来的1张牌是：{remembered_card}")
    # print(f"剩下7张牌是：{random_8_cards}")

    # 4. 南方人取1张，北方人取2张，无法确定取3张，将这些牌随机插入剩下的牌中
    location = int(random.randint(1, 4))
    first_location = [random_8_cards.popleft() for i in range(location)]
    # print(f"上面地区牌是：{first_location}")
    # print(f"剩下牌是：{random_8_cards}")

    for card in first_location:
        insert_position = random.randint(1, len(random_8_cards) - 2)
        random_8_cards.insert(insert_position, card)
    #     print(f"插入牌是：{card}，随机插入位置是：{insert_position + 1}，新牌顺序是{random_8_cards}")
    # print(f"根据南北方，随机插入剩下牌中间，此时新牌顺序：{random_8_cards}")

    # 5. 男生取1张，女生取2张，将这些牌扔掉
    gender = int(random.randint(1, 2))
    for i in range(gender):
        random_8_cards.popleft()
    # print(f"根据性别扔牌，此时新牌顺序：{random_8_cards}")

    # 6. 见证奇迹的时刻
    # 将双端队列中的元素向左旋转7个位置
    random_8_cards.rotate(-7)
    # print(f"见证奇迹的时刻（向左旋转7次牌），此时新牌顺序：{random_8_cards}")

    # 7. 好运留下来，烦恼丢出去！
    while len(random_8_cards) > 1:
        random_8_cards.append(random_8_cards.popleft())  # 第一张牌移到最后
        random_8_cards.popleft()  # 删除现在的第一张牌
    #     print(f"好运留下来，烦恼丢出去！（第一张牌移到最后，删除现在的第一张牌）此时剩余牌顺序：{random_8_cards}")
    # print(f"剩余最后1张牌是：{random_8_cards[0]}")

    # 8. 查看藏起来的1张牌
    # print(f"藏起来的1张牌是：{remembered_card[0]}")
    return [random_8_cards[0], remembered_card]


if __name__ == '__main__':
    # 进行多次模拟,计算正确率
    times = 100000
    correct_match_times = 0
    for i in range(times):
        result = magic()
        if result[0] == result[1]:
            correct_match_times += 1
    match_rate = f"{(correct_match_times / times * 100)} % "
    print(f"运行{times}次,正确率是{match_rate}")