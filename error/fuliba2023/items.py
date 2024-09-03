# -*- coding: utf-8 -*-
import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    publish_time = scrapy.Field()
    videos = scrapy.Field()