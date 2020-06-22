# -*- coding: utf-8 -*-
import datetime
from wangyi.items import WangyiItem
import scrapy
import re


class WangyispiderSpider(scrapy.Spider):
    name = 'wangyispider'
    allowed_domains = ['auto.163.com']
    start_urls = [
        # 新车新闻
        'https://auto.163.com/newcar',
        'https://auto.163.com/special/2016nauto_02/#subtab',
        'https://auto.163.com/special/2016nauto_03/#subtab',
        'https://auto.163.com/special/2016nauto_04/#subtab',

        # 购车新闻
        'https://auto.163.com/buy',
        'https://auto.163.com/special/2016buy_02/#subtab',
        # 试驾新闻
        'https://auto.163.com/test',
        'https://auto.163.com/special/2016drive_02/#subtab',
        # 导购新闻
        'https://auto.163.com/guide',
        'https://auto.163.com/special/2016buyers_guides_02/#subtab',
        # 新能源新闻
        'https://auto.163.com/elec',
        'https://auto.163.com/special/auto_newenergy_02/#subtab',
        # 行业新闻
        'https://auto.163.com/news',
        'https://auto.163.com/special/2016news_02/#subtab',
        'https://auto.163.com/special/2016news_03/#subtab',
        'https://auto.163.com/special/2016news_04/#subtab',
        'https://auto.163.com/special/2016news_05/#subtab',
        'https://auto.163.com/special/2016news_06/#subtab',
        'https://auto.163.com/special/2016news_07/#subtab',
        'https://auto.163.com/special/2016news_08/#subtab',
        'https://auto.163.com/special/2016news_09/#subtab',
        'https://auto.163.com/special/2016news_10/#subtab',
    ]

    def parse(self, response):

        item_cont = response.xpath('//div[@class="item-cont"]')
        for data in item_cont:
            request_url = response.request.url
            item = {}
            item['URL'] = data.xpath('./h3/a/@href').extract_first()
            item['TITLE'] = data.xpath('./h3/a//text()').extract_first()
            item['KEY_WORDS'] = data.xpath('./div[@class="item-tag"]/a/text()').extract()
            item['KEY_WORDS'] = ','.join(item['KEY_WORDS'])
            item['PUBLISH_TIME'] = data.xpath('.//span[@class="item-time"]//text()').extract_first()
            item['READ_NUM'] = data.xpath('.//span[@class="item-comment"]//text()').extract_first()
            if 'newcar' in request_url or 'nauto' in request_url:
                item['FLLJ'] = '新车新闻'
            elif 'buy' in request_url:
                item['FLLJ'] = '购车新闻'
            elif 'test' in request_url or 'drive' in request_url:
                item['FLLJ'] = '试驾新闻'
            elif 'guide' in request_url:
                item['FLLJ'] = '导购新闻'
            elif 'elec' in request_url or 'newenergy' in request_url:
                item['FLLJ'] = '新能源新闻'
            elif 'news' in request_url:
                item['FLLJ'] = '行业新闻'
            print('********************************')

            yield scrapy.Request(
                item['URL'],
                callback=self.parse_detail,
                dont_filter=False,
                meta=item,
            )

    def parse_detail(self, response):
        CONTENT = ''
        meta_dict = response.meta
        item = WangyiItem()
        item['URL'] = meta_dict['URL']
        item['TITLE'] = meta_dict['TITLE']
        item['FLLJ'] =  meta_dict['FLLJ']
        item['READ_NUM'] = meta_dict['READ_NUM']
        item['PUBLISH_TIME'] = meta_dict['PUBLISH_TIME']
        item['KEY_WORDS'] = meta_dict['KEY_WORDS']
        item['DATA_SOURCE'] = '网易汽车'
        item['COMMENTS_NUM'] = '0'
        item['IMAGE_URL'] = ''
        item['CRAWLER_TIME'] = str(datetime.date.today())
        try:
            CONTENT_HTML = response.xpath('//div[@id="endText"]').getall()
            print(CONTENT_HTML[0])
            pat = re.sub(r'\n', '<br/>', CONTENT_HTML[0])
            # pat = re.sub(' ', '', pat)
            pat = re.sub('\"', '“', pat)
            item['CONTENT_HTML'] = pat
            # print(CONTENT_HTML[0])
            # print('1111111111111111')
            IMAGE_URL = re.findall('<img src="(.*?)" alt=".*?">',CONTENT_HTML[0])
            if IMAGE_URL ==[]:
                IMAGE_URL = re.findall('<img alt=".*?" src="(.*?)"></p>',CONTENT_HTML[0])
            pat1 = re.sub(r'\n', '<br/>', IMAGE_URL[0])
            # pat1 = re.sub(' ', '', pat1)
            pat1 = re.sub('\"', '“', pat1)
            item['IMAGE_URL'] = pat1
            print(pat1)
            print('11111111111111111111')
            item['CONTENT'] = response.xpath('//div[@id="endText"]//text()').extract()
            for data in item['CONTENT']:
                if data.strip():
                    CONTENT += data.strip()

            item['CONTENT'] = CONTENT
        except Exception as e:
            item['CONTENT'] = ''
            print(e)
        # print(item)

        return item




