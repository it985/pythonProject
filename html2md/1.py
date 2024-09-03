import html2text as ht

def html_2_text(input_file, output_file):
    text_maker = ht.HTML2Text()
    # 读取html格式文件
    with open(input_file, 'r', encoding='UTF-8') as f:
        htmlpage = f.read()
    # 处理html格式文件中的内容
    text = text_maker.handle(htmlpage)
    # 写入处理后的内容
    with open(output_file, 'w', encoding='UTF-8') as f:
        f.write(text)


if __name__ == "__main__":
    input_file = "./html2md/html/2022-12-15_pixiv每日精选图片第58期.html"
    output_file = "./html2md/html/result.md"

    html_2_text(input_file, output_file)

