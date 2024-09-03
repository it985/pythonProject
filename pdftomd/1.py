import PyPDF2
from PyPDF2 import PdfReader
import re

def convert_pdf_to_md(pdf_path, md_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()

    # Clean up the extracted text
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\n ', '\n', text)
    text = re.sub(r' +', ' ', text)

    # Write the text to the Markdown file
    with open(md_path, 'w', encoding='utf-8') as file:
        file.write(text)
# 示例用法
pdf_path = 'redis.pdf'
md_path = './redis.md'
convert_pdf_to_md(pdf_path, md_path)
