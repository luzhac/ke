# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KeqqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()


class KesumItem(scrapy.Item):
    itime = scrapy.Field()
    batch = scrapy.Field()
    source = scrapy.Field()
    cat=scrapy.Field()
    title=scrapy.Field()
    keshi=scrapy.Field()
    renshu=scrapy.Field()
    organiger=scrapy.Field()
    mianfei=scrapy.Field()
    bref=scrapy.Field()
