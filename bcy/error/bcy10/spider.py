# -*- coding: utf-8 -*-
import scrapy
from sec_bcy.items import BcyItem


class BcyspiderSpider(scrapy.Spider):
    name = 'bcySpider'

    page_index = 2
    url = 'https://bcy.net/coser/allwork?&p={0}'
    start_urls = [url.format(str(page_index))]

    # coser列表翻页
    def parse(self, response):
        while self.page_index < 3:
            page_url = self.url.format(str(self.page_index))
            yield scrapy.Request(page_url, callback=self.parse_page)
            self.page_index += 1

    # 获取coser个人页面集合
    def parse_page(self, response):
        corser_list = response.xpath("//a[contains(@href,'/u/')]/@href").extract()
        # 去重
        corser_list = list(set(corser_list))
        for coser in corser_list:
            coser_url = "https://bcy.net" + coser
            yield scrapy.Request(coser_url, callback=self.parse_detail, meta={'JsPage': True})

    # 进入单个coser界面
    def parse_detail(self, response):
        # item=BcyItem()
        # item['name'] = response.xpath("//a[@class='fz18 lh1d2 white']/text()").extract()[0]
        # item['coser_url'] = response.url
        # item['detail_urls']=response.xpath("//a[contains(@href,'detail')]/@href").extract()
        # item['detail_urls']=list(set(item['detail_urls']))
        # item['followers']=response.xpath("//a[contains(@href,'follower')]/span[2]/text()").extract()[0]
        # item['summary'] = ''.join(response.xpath("//p[@class='fz12 lh1d4 mt12 maxh32 ovf']/text()").extract())
        # item['img_urls']=[]
        detail_urls = response.xpath("//a[contains(@href,'detail')]/@href").extract()

        detail_urls = list(set(detail_urls))
        for each in detail_urls:
            url = "https://bcy.net" + each
            yield scrapy.Request(url, callback=self.parse_pic)
            # yield scrapy.Request(url, callback=self.parse_pic, meta={'item': item, 'isEnd': True})
            # 判断是否是最后一个url，如果是则附带一个meta key
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # scrapy为异步请求，这里的request顺序混乱，isEnd为True的request容易跑到值为False的前面

            # url = "https://bcy.net" + each
            # if (item['detail_urls'].index(each)) == (len(item['detail_urls']) - 1):
            #     yield scrapy.Request(url, callback=self.parse_pic, meta={'item': item,'isEnd':True})
            # else:
            #     yield scrapy.Request(url, callback=self.parse_pic, meta={'item': item,'isEnd':False})

    def parse_pic(self, response):
        item = BcyItem()
        name = response.xpath("//a[@class='fz14 dib maxw250 cut']/text()").extract()
        if len(name) > 0:
            item['name'] = name[0]
        else:
            item['name'] = response.xpath("//a[@class='lh24 fz14 name dib mr5']/text()").extract()[0]
        item['detail_url'] = response.url
        img_urls = response.xpath("//img[@class='detail_std detail_clickable']/@src").extract()
        item['img_urls'] = [url.replace('/w650', '') for url in img_urls]
        yield item
        # item=response.meta['item']
        # isEnd=response.meta['isEnd']
        # pic_list=response.xpath("//img[@class='detail_std detail_clickable']/@src").extract()
        # for pic in pic_list:
        #     item['img_urls'].append(pic.replace('/w650',''))
        # if isEnd == True:
        #     yield item
        #     time.sleep(2)