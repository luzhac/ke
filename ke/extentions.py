import logging
from scrapy import signals
from scrapy import crawler
from scrapy.exceptions import NotConfigured
import pymongo

logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):

    def __init__(self, item_count,stats):
        self.item_count = item_count
        self.items_scraped = 0
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
        stats=crawler.stats
        # instantiate the extension object
        ext = cls(item_count,stats)

        # connect the extension object to signals

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        # return the extension object
        return ext


    def spider_closed(self, spider):
        a=self.stats.get_stats()
        a['name']=spider.__class__.__name__
        a['batch']=spider.arg
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['ke']
        collection = db['ke_log']
        collection.insert(a)
        logger.info("I ßclosed spider %s", spider.name)

