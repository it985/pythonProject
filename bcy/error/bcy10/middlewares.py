# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging, time
from scrapy.http import HtmlResponse


class myMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        if 'JsPage' in request.meta:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(request.url)
            # time.sleep(1)
            body = driver.page_source
            # driver.close()        不知道在什么时候释放资源
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


class SecBcySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    # 设置使用chrome headless

    # 进入网站
    # driver.get()
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(response.url)
        content = driver.page_source.encode('utf-8')
        driver.quit()
        logging.warning('!' * 88 + response.url)

        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SecBcyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print('!' * 88 + "from_crawler233")
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('!' * 88 + "process_request")

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.get(request.url)
        # content = driver.page_source.encode('utf-8')
        # driver.quit()

        return None

    def process_response(self, request, response, spider):
        print('!' * 88 + "process_response")
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        print('!' * 88 + "process_exception")
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        print('!' * 88 + "spider_opened")
        spider.logger.info('Spider opened: %s' % spider.name)