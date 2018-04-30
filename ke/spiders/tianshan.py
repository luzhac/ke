from scrapy import Spider, Request
from ke.items import  KeqqItem
from ke.items import  KesumItem
from pyquery import PyQuery as pq
import re
from datetime import datetime

class TianshanSpider(Spider):
    name = 'tianshan'
    allowed_domains = ['edu.hellobi.com']
    start_urls = ['https://edu.hellobi.com/course/explore']

    def __init__(self, arg=None):
        if arg is None:
            self.arg = int(0)
        else:
            self.arg = int(arg)

    def start_requests(self):
        url = 'https://edu.hellobi.com/course/explore'
        yield Request(url, self.parse_category)

    def parse_category(self,response):
        dd=response.css('div.category-list.mt10:nth-child(2) li')
        for item in dd:
            if item.css('a::text').extract_first()!='全部':
                print(item.css('a::text').extract_first())
                url=item.css('a::attr(href)').extract_first()
                yield Request(url,self.parse_summary)


    def parse_summary(self,response):
        cat=response.css('div.category-list.mt10 ul.list-inline.pull-left li.active a::text').extract_first()
        dd=response.css('div.mt30 ul.course-list')
        for item in dd:
            #print("价格",item.css('span.pull-right.price::text').extract_first())
            #todo finish none can't have group()
            if re.search('[\d\.]+',item.css('span.pull-right.price::text').extract_first()) is None:
                mianfei=0
            else:
                mianfei=float(re.search('[\d\.]+',item.css('span.pull-right.price::text').extract_first()).group())
            title = str.strip(item.css('h3 a::text').extract_first())
            #print('keshi',re.search('\d+',item.css('span.length::text').extract_first()).group())
            if re.search('\d+',item.css('span.length::text').extract_first()) is None:
                keshi=0
            else:
                keshi=int(re.search('\d+',item.css('span.length::text').extract_first()).group())
            if re.search('[\d\.]+',item.css('div span.pull-right.people::text').extract_first()) is None:
                renshu=0
            else:
                renshu=int(re.search('[\d\.]+',item.css('div span.pull-right.people::text').extract_first()).group())
            if item.css('span.teacher a::text').extract_first() is None:
                teacher=''
            else:
                teacher=item.css('span.teacher a::text').extract_first()
            href = item.css('.thumbnail.course-box a::attr(href)').extract_first()
            #print(mianfei,title,keshi,renshu,teacher,href)
            item = KesumItem()
            item['batch'] = self.arg
            item['source'] = 'tianshan'
            item['itime'] = datetime.utcnow()
            item['cat'] =cat
            item['title'] = title
            item['keshi'] = keshi
            item['mianfei'] = mianfei
            item['renshu'] = renshu
            item['organiger'] = teacher
            item['bref'] = href
            yield item

        next_page = response.css('ul.pagination li a[rel="next"]::attr(href)').extract_first()
        if next_page is not None:
            yield Request(next_page, self.parse_summary)

