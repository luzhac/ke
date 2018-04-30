# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json
from ke.items import  KesumItem
from datetime import datetime

class Study163Spider(scrapy.Spider):
    name = 'study163'
    allowed_domains = ['study.163.com']
    #start_urls = ['http://study.163.com/']
    HEADERS = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Origin': 'http://study.163.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
               'Content-Type': 'application/json',
               'Referer': 'http://study.163.com/category/ppt',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'

               }

    url = 'http://study.163.com/p/search/studycourse.json'

    def __init__(self, arg=None):
        if arg is None:
            self.arg = int(0)
        else:
            self.arg = int(arg)

    def start_requests(self):
        #url='http://study.163.com/'
        # 因为每个分目录都有各目录的信息，直接调用parse_category2
        url='http://study.163.com/category/office-productivity'
        yield Request(url,self.parse_category3)

    def parse_category1(self,response):
        #print(response.body_as_unicode())
        dd=response.css('div.inn .f-f0.first')
        for item in dd:
            link=item.css('a::attr(href)').extract_first()
            title=item.css('a::text').extract_first()
            print('1 ',link,title)
            url=response.urljoin(link)
            yield Request(url,self.parse_category2)

    def parse_category2(self,response):
        #print(response.body_as_unicode())
        dd=response.css('li.level2-item a')
        for item in dd:
            link=item.css('a::attr(href)').extract_first()
            title=item.css('a::text').extract_first()
            print('2 ',link,title)
            url=response.urljoin(link)
            if title!='精选好课':
                yield Request(url, self.parse_category3)
    def parse_category3(self,response):
        ff=response.css('li.level-item')

        cat=response.css('li.navcrumb-item a[href="javascript:void(0)"]::text').extract_first()+' '+response.css('li.level2-item a::text').extract_first()
        print(cat)
        for item in ff:
            link = item.css('a::attr(href)').extract_first()
            title = item.css('a::text').extract_first()
            id = item.css('li[id]::attr(id)').extract_first()
            if id is not None:
                id=re.search('[\d]+',id).group()
                url = response.urljoin(link)
                print('3', url, title, id)
                data = '{"pageIndex":%d,"pageSize":50,"relativeOffset":%d,"frontCategoryId":"%d","searchTimeType":-1,"orderType":0,"priceType":-1,"activityId":0}' % (
                1, 0,int(id))
                print(data)
                yield Request(self.url, method='POST', body=data,
                              callback=self.parse_first, headers=Study163Spider.HEADERS,meta={'cat': cat,'cat_id': id,'dont_merge_cookies': True})



    def parse_first(self, response):
        #print(response.body_as_unicode())

        jsonresponse = json.loads(response.body_as_unicode())
        max_page=jsonresponse['result']['query']['totlePageCount']
        for li in jsonresponse['result']['list']:
            item = KesumItem()
            item['title'] = li['productName']
            item['batch'] = self.arg
            item['itime'] = datetime.utcnow()
            item['source'] = 'study163'
            item['cat'] = response.meta['cat']
            item['keshi'] = ''
            if li['learnerCount'] is None:
                item['renshu'] = 0
            else:
                item['renshu'] = int(li['learnerCount'])
            item['organiger'] = li['provider']
            if li['originalPrice'] is None:
                item['mianfei'] =float(0)
            else:
                item['mianfei'] = float(li['originalPrice'])
            item['bref'] =response.urljoin('/course/introduction/'+str(li['courseId'])+'.htm')
            yield item
            print(li['productId'],li['productName'],li['originalPrice'],li['learnerCount'],li['provider'])
        for i in range(2, max_page + 1):
            j=50*(i-1)
            data = '{"pageIndex":%d,"pageSize":50,"relativeOffset":%d,"frontCategoryId":"%d","searchTimeType":-1,"orderType":0,"priceType":-1,"activityId":0}' %( i ,j,int(response.meta['cat_id']))
            print('page', i, data)
            yield Request(Study163Spider.url, method='POST', body=data,
                          callback=self.parse, headers=Study163Spider.HEADERS,dont_filter='True', meta={'dont_merge_cookies': True,'cat':response.meta['cat']})

    def parse(self,response):
        jsonresponse = json.loads(response.body_as_unicode())
        max_page = jsonresponse['result']['query']['totlePageCount']
        for li in jsonresponse['result']['list']:
            item = KesumItem()
            item['title'] = li['productName']
            item['itime']=datetime.utcnow()
            item['batch'] = self.arg
            item['source'] = 'study163'
            item['cat'] = response.meta['cat']
            item['keshi'] = ''
            if li['learnerCount'] is None:
                item['renshu'] = 0
            else:
                item['renshu'] = int(li['learnerCount'])
            item['organiger'] = li['provider']
            if li['originalPrice'] is None:
                item['mianfei'] =float(0)
            else:
                item['mianfei'] = float(li['originalPrice'])
            item['bref'] = response.urljoin('/course/introduction/' + str(li['courseId']) + '.htm')
            try:
                yield item
            except Exception as e:
                print(e)
            print(li['productId'], li['productName'], li['originalPrice'], li['learnerCount'], li['provider'])

    def parse_summary(self,response):
        print(response.body_as_unicode())
        dd=response.css('div.uc-coursecard.uc-ykt-coursecard.f-fl')
        #print(dd)
        for item in dd:
            print('1')
            title = item.css('div.uc-ykt-coursecard-wrap_tit h3::text').extract_first()
            print(title)
            break


