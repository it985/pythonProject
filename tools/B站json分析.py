import json


def extract_mids_from_json(json_data):
    """
    从JSON数据中提取所有mid值

    Args:
        json_data: JSON格式的数据

    Returns:
        包含所有mid的列表
    """
    # 解析JSON数据
    data = json.loads(json_data)

    # 提取所有mid值
    mids = [str(item["mid"]) for item in data]

    return mids


def main():
    # 从文件读取JSON数据
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            json_data = f.read()

        # 提取mid列表
        mid_list = extract_mids_from_json(json_data)

        # 打印结果
        print(f"共提取到 {len(mid_list)} 个mid")
        print("mid列表:", mid_list)

        # 将mid列表保存到文件，以英文逗号分隔，不换行
        with open('mids.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(mid_list))
        print("已将mid列表保存到 mids.txt")

    except FileNotFoundError:
        print("未找到data.json文件")
    except json.JSONDecodeError:
        print("JSON格式错误，无法解析")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()