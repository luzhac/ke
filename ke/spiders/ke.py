# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from ke.items import  KeqqItem
from ke.items import  KesumItem
from pyquery import PyQuery as pq
import re
from datetime import datetime

class KeSpider(Spider):
    name = 'ke'
    allowed_domains = ['ke.qq.com']
    start_urls = ['http://ke.qq.com/']

    def __init__(self, arg=None):
        if arg is None:
            self.arg = 0
        else:
            self.arg = arg

    def start_requests(self):
        url='https://ke.qq.com/course/list?'
        #url='https://ke.qq.com/course/list?mt=1001&st=2004&tt=3024'
        yield Request(url,self.parse_category)


    def parse_category(self, response):
        dd=response.css('dd[class=""]')
        dd_more = response.css('dd[class="curr"]')
        lower_level_urls = response.css('dd[class=""] a::attr(href)').extract()
        lower_level_urls_more = response.css('dd[class="curr"] a::attr(href)').extract()
        url_short=re.search('.*\/\/.*?(\/.*)',response.url).group(1)

        if url_short in lower_level_urls+lower_level_urls_more:
            print('test')
            yield Request(url=response.url,dont_filter='True',callback=self.parse_sumary)
        else:
            for node in dd+dd_more:
                #todo how to encode to display chinese
                title=node.css('a::attr(title)').extract_first()
                short_url = node.css('a::attr(href)').extract_first()
                url = response.urljoin(short_url)
                item=KeqqItem()
                item['title'] = title
                item['url'] = url
                #print(url)
                #yield item
                yield Request(url,self.parse_category)
    def parse_sumary(self,response):

        doc = pq(response.body_as_unicode())
        next_page = doc('.page-next-btn.icon-font.i-v-right').attr('href')
        #print(doc)
        cat = ''
        for item in doc('a.mod-breadcrumbs__nav').items():
            if item.attr('title') != '全部课程':
                cat = cat + item.attr('title') + ' '
        doc.remove('dd.curr_all')
        doc.remove('aside.main-right')
        doc.remove('section.main-below')
        lis = doc('li.course-card-item').items()
        for li in lis:
            doc = pq(li)
            # 默认费用是0，包括'免费'
            mianfei = '0'
            # todo if change + to *, none result
            try:
                mianfei = re.search('[\d\.]+', doc('span.line-cell.item-price').text()).group()
            except Exception as e:
                print(doc('img.item-img').attr('title'), e)
            keshi = 0
            try:
                keshi = re.search('\d+(?=节)', doc('span.item-status-step').text()).group()
            except Exception as e:
                print(doc('img.item-img').attr('title'), e)

            item=KesumItem()
            item['batch'] = self.arg
            item['source'] = '腾讯'
            item['itime'] = datetime.utcnow()
            item['cat'] = cat
            item['title'] = doc('img.item-img').attr('title')
            item['keshi'] = keshi
            if re.search('\d+', doc('span.line-cell.item-user').text()).group() is None:
                item['renshu'] = int(0)
            else:
                item['renshu'] = int(re.search('\d+', doc('span.line-cell.item-user').text()).group())
            item['organiger'] = doc('a.item-source-link').text()
            if mianfei is None:
                item['mianfei'] =float(0)
            else:
                item['mianfei'] = float(mianfei)
            item['bref'] = doc('a.item-img-link').attr('href')
            #todo 判断叶子节点
            if len(response.url)>50:
                try:
                    yield item
                except Exception as e:
                    print(e)


        if next_page!='javascript:void(0);':
            next_page=response.urljoin(next_page)
            yield Request(next_page,self.parse_sumary)