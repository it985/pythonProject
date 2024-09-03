import html2text as ht
text_maker = ht.HTML2Text()
# 读取html格式文件
with open('./html/2022-12-15_pixiv每日精选图片第58期.html', 'r', encoding='UTF-8') as f:
    htmlpage = f.read()
# 处理html格式文件中的内容
text = text_maker.handle(htmlpage)
# 写入处理后的内容
with open('*.md', 'w') as f:
    f.write(text)