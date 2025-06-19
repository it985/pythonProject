# """
# B站用户信息批量查询工具（基于 bilibili-api-python）
# 需要先安装库：pip install bilibili-api-python
# """
#
# from bilibili_api import user, sync
# import time
#
#
# def get_user_info(uid):
#     """
#     获取B站用户信息（名称和粉丝数）
#     :param uid: 用户UID
#     :return: (用户名称, 粉丝数)
#     """
#     try:
#         u = user.User(uid=uid)
#         # 同步获取用户基础信息
#         info = sync(u.get_info())
#         # 同步获取用户关系数据（包含粉丝数）
#         stat = sync(u.get_relation())
#         return info['name'], stat['follower']
#     except Exception as e:
#         raise RuntimeError(f"接口请求失败: {str(e)}") from e
#
#
# if __name__ == "__main__":
#     # 需要查询的UID列表（替换为实际需要查询的UID）
#     uids = [
#         451320374,  # 测试有效UID
#         123456789,  # 测试不存在UID
#         546195  # 测试有效UID（例如B站官方账号）
#     ]
#
#     for idx, uid in enumerate(uids):
#         try:
#             start_time = time.time()
#             name, followers = get_user_info(uid)
#             print(f"[{idx + 1}/{len(uids)}] {name}：{uid}：{followers}")
#         except Exception as e:
#             print(f"[{idx + 1}/{len(uids)}] 获取UID {uid} 失败：{str(e)}")
#
#         # 添加请求间隔避免触发风控（建议1-3秒）
#         time.sleep(1)
#
#     print("\n查询完成，无效的UID会自动显示错误信息")
import time

import requests


def get_user_info(uid):
    """
    获取B站用户信息
    :param uid: 用户UID
    :return: 用户名称和粉丝数的元组，获取失败则返回None
    """
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data["code"] == 0:
            name = data["data"]["name"]

            # 获取粉丝数需要另一个API请求
            stat_url = f"https://api.bilibili.com/x/relation/stat?vmid={uid}"
            stat_response = requests.get(stat_url, headers=headers)
            stat_data = stat_response.json()

            if stat_data["code"] == 0:
                follower = stat_data["data"]["follower"]
                return name, follower
    except Exception as e:
        print(f"获取用户 {uid} 信息时出错: {e}")

    return None


def main():
    # 输入多个UID，以逗号分隔
    uids_input = input("请输入B站用户UID(多个UID用逗号分隔): ")
    uids = [uid.strip() for uid in uids_input.split(",")]

    print("\n===== B站用户信息 =====")

    for uid in uids:
        result = get_user_info(uid)
        if result:
            name, follower = result
            print(f"{name}：{uid}：{follower}")
        else:
            print(f"无法获取用户 {uid} 的信息")

        # 添加延时，避免请求过于频繁
        time.sleep(1)


if __name__ == "__main__":
    main()
