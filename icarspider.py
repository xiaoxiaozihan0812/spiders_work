# -*- coding: utf-8 -*-
import datetime

import scrapy
import re


class IcarspiderSpider(scrapy.Spider):
    name = 'icarspider'
    allowed_domains = ['xcar.com.cn']

    start_urls = [
        'http://info.xcar.com.cn/list/164_1/', # 国内新车
        'http://info.xcar.com.cn/list/234_1/', # 海外新车
        'http://info.xcar.com.cn/push_558_1/', # 爱卡谍照
        'http://suv.xcar.com.cn/news_1/',     # suv 新车
        'http://suv.xcar.com.cn/guide_1/',      # 对比导购
        'http://suv.xcar.com.cn/drive_1/',      #  试驾新闻
        'http://info.xcar.com.cn/list/214_1/',  # 行业新闻
        'http://info.xcar.com.cn/push_559_1/',    # 新车点评
        'http://info.xcar.com.cn/list/848_1/',   # 爱卡头条
        'http://info.xcar.com.cn/push_562_1/',  # 深度观察
        'http://info.xcar.com.cn/push_650_1/',  # 五问五答
        'http://newcar.xcar.com.cn/list/239_1/', # 车型海选
        'http://newcar.xcar.com.cn/list/811_1/', # 对比选购
        'http://newcar.xcar.com.cn/list/243_1/', # 深度感受
        'http://newcar.xcar.com.cn/list/245_1/', # 购车手册
        'http://newcar.xcar.com.cn/list/858_1/',  # 实拍体验
        'http://drive.xcar.com.cn/list/845_1/',  #  专业测试
        'http://drive.xcar.com.cn/list/120_1/', # 试驾体验
        # 'http://info.xcar.com.cn/list/164_2/',
        # 'http://info.xcar.com.cn/list/164_3/',
        # 'http://info.xcar.com.cn/list/164_4/',
        # 'http://info.xcar.com.cn/list/164_5/',
        # 'http://info.xcar.com.cn/list/164_6/',
        # 'http://info.xcar.com.cn/list/234_2/',
        # 'http://suv.xcar.com.cn/news_2/',
        # 'http://suv.xcar.com.cn/news_3/',
        # 'http://suv.xcar.com.cn/news_4/',
        # 'http://info.xcar.com.cn/list/214_2/',
        # 'http://info.xcar.com.cn/list/214_3/',

    ]

    def parse(self, response):
        request_url = response.request.url
        li_list = response.xpath('//li[@class="clearfix moreImgSize"]')
        for li in li_list:
            item = {}
            # 标题
            item['TITLE'] = li.xpath('.//dt/a//text()').extract_first().strip()
            # 链接
            item['URL'] = li.xpath('.//dt/a//@href').extract_first().strip()
            print(item['URL'])
            # 时间
            item['PUBLISH_TIME'] = li.xpath('.//dd[@class="listIcon"]//text()').extract()[1].strip()
            item['PUBLISH_TIME'] = item['PUBLISH_TIME'].split(' ')[0]
            # 阅读数
            try:
                item['READ_NUM'] = li.xpath('.//span[@class="remark_object"]/a[2]//text()').extract_first().strip()
                if 'w' in item['READ_NUM']:
                    item['READ_NUM'] = str(int(float(item['READ_NUM'][:-1]) * 10000))
            except Exception as e:
                item['READ_NUM'] = '0'
                print(e)
            item['IMAGE_URL'] = 'http:' + li.xpath('.//div[@class="leftConSize"]//img//@src').extract_first().strip()
            if '164' in request_url:
                item['FLLJ'] = '国内新车'
            elif '234' in request_url:
                item['FLLJ'] = '国外新车'
            elif 'push_558' in request_url:
                item['FLLJ'] = '新车谍照'
            elif 'news' in request_url:
                item['FLLJ'] = 'suv 新车'
            elif 'guide' in request_url:
                item['FLLJ'] = '对比导购'
            elif 'drive' in request_url:
                item['FLLJ'] = '试驾新闻'
            elif '214' in request_url:
                item['FLLJ'] = '行业新闻'
            elif 'push_559' in request_url:
                item['FLLJ'] = '新车点评'
            elif '848' in request_url:
                item['FLLJ'] = '爱卡头条'
            elif 'push_562' in request_url:
                item['FLLJ'] = '深度观察'
            elif 'push_650' in request_url:
                item['FLLJ'] = '五问五答'
            elif '239' in request_url:
                item['FLLJ'] = '车型海选'
            elif '811' in request_url:
                item['FLLJ'] = '对比选购'
            elif '243' in request_url:
                item['FLLJ'] = '深度感受'
            elif '245' in request_url:
                item['FLLJ'] = '购车手册'
            elif '858' in request_url:
                item['FLLJ'] = '实拍体验'
            elif '811' in request_url:
                item['FLLJ'] = '对比选购'
            elif '845' in request_url:
                item['FLLJ'] = '专业测试'
            elif '120' in request_url:
                item['FLLJ'] = '试驾体验'
            else:
                item['FLLJ'] = '行业新闻'

            yield scrapy.Request(
                item['URL'],
                callback=self.parse_detail,
                dont_filter=False,
                meta=item,
            )

    def parse_detail(self, response):
        meta_dict = response.meta
        item = {}
        item['URL'] = meta_dict['URL']
        item['TITLE'] = meta_dict['TITLE']
        item['KEY_WORDS'] = ''
        item['DATA_SOURCE'] = '爱卡汽车'
        item['READ_NUM'] = meta_dict['READ_NUM']
        item['IMAGE_URL'] = meta_dict['IMAGE_URL']
        item['COMMENTS_NUM'] = '0'
        item['CRAWLER_TIME'] = str(datetime.date.today())
        item['FLLJ'] = meta_dict['FLLJ']
        item['PUBLISH_TIME'] = meta_dict['PUBLISH_TIME']
        item['CONTENT'] = ''
        try:
            #wz带样式的内容
            CONTENT_HTML = response.xpath('//div[@class="artical_player_wrap"]').getall()
            con = re.split('精彩内容回顾',CONTENT_HTML[0])
            pat = re.sub(r'\n', '<br/>', con[0])
            # pat = re.sub(' ', '', pat)
            pat = re.sub('\"', '“', pat)
            item['CONTENT_HTML'] = pat
            CONTENT_LIST = response.xpath('//div[@class="artical_player_wrap"]//text()').extract()
            for con in CONTENT_LIST:
                item['CONTENT'] += con.strip()
        except Exception as e:
            print(e)
        return item





