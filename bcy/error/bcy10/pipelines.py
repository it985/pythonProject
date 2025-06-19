# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import requests


class SecBcyPipeline(object):
    def __init__(self):
        self.output = open('corser.json', 'w', encoding='utf-8')
        self.num = 0
        self.path = 'H:/CRAWL/pic/'

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.output.write(jsontext)
        if len(item['img_urls']) != 0:
            dir_path = self.path + item['name']
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for each in item['img_urls']:
                self.num += 1
                with open(dir_path + '/' + each[-36:].replace('/', '-'), 'wb') as handle:
                    print(str(self.num) + ":" + dir_path + '/' + each[-36:])
                    response = requests.get(
                        each,
                        stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item

    def close_spider(self, spider):
        self.output.close()