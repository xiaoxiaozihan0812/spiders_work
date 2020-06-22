# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
import json
from chexun.items import ChexunItem
import re

class ChexunspiderSpider(scrapy.Spider):
    name = 'chexunspider'
    allowed_domains = ['chexun.com']
    start_urls = [
        'http://api.tool.chexun.com/news/getNewsInfo.do?num=10&type=1&seriesId=0&ccfFlag=1&subType=1', # 新闻
        'http://api.tool.chexun.com/news/getNewsInfo.do?num=10&type=2&seriesId=0&ccfFlag=1&subType=1', # 导购
        'http://api.tool.chexun.com/news/getNewsInfo.do?num=10&type=3&seriesId=0&ccfFlag=1&subType=1', # 评测
        'http://api.tool.chexun.com/news/getNewsInfo.do?num=10&type=4&seriesId=0&ccfFlag=1&subType=1', # 用车
    ]

    def parse(self, response):
        data_list = json.loads(response.text)
        for data in data_list:
            # url
            item = {}
            item['PUBLISH_TIME'] = time.strftime("%Y-%m-%d", time.localtime(data['time']//1000))
            # time.strftime("%Y-%m-%d", data['time']//1000)
            item['URL'] = data['url']
            item['TITLE'] = data['title']
            # 新闻类型
            item['FLLJ'] = data['pname']
            # 关键字
            item['KEY_WORDS'] = data['subhead']
            # 照片链接
            item['IMAGE_URL'] = data['coverpic']
            # 阅读数
            item['READ_NUM'] = '0'
            try:
                item['READ_NUM'] = data['pageView']
                if '万' in item['READ_NUM']:
                    item['READ_NUM'] = str(int((float(item['READ_NUM'][:-1]) * 10000)))
            except Exception as e:
                print(e)
            yield scrapy.Request(
                item['URL'],
                callback=self.parse_detail,
                dont_filter=False,
                meta=item,
            )

    def parse_detail(self, response):
        meta_dict = response.meta
        item = ChexunItem()
        item['URL'] = meta_dict['URL']
        item['TITLE'] = meta_dict['TITLE']
        item['PUBLISH_TIME'] = meta_dict['PUBLISH_TIME']
        item['KEY_WORDS'] = meta_dict['KEY_WORDS']
        item['DATA_SOURCE'] = '车讯网'
        item['READ_NUM'] = meta_dict['READ_NUM']
        item['COMMENTS_NUM'] = '0'
        item['IMAGE_URL'] = meta_dict['IMAGE_URL']
        item['CRAWLER_TIME'] = str(datetime.date.today())
        item['FLLJ'] = meta_dict['FLLJ']
        item['CONTENT'] = ''
        try:
         
            CONTENT_HTML = response.xpath('//div[@class="article-content"]').getall()
            pat = re.sub(r'\n', '<br/>', CONTENT_HTML[0])
            # pat = re.sub(' ', '', pat)
            pat = re.sub('\"', '“', pat)
            item['CONTENT_HTML'] = pat
            # item['CONTENT_HTML'] = CONTENT_HTML[0]
            CONTENT_LIST = response.xpath('//div[@class="article-content"]//text()').extract()
            for con in CONTENT_LIST:
                item['CONTENT'] += con.strip()
        except Exception as e:
            print(e)
        return item

