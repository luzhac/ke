
from celery_app import app
import os
import pymongo


client = pymongo.MongoClient(host='localhost', port=27017)
db = client['ke']
collection = db['ke']


@app.task()
def crawl1():
    a=0
    print('asdfadsfadsfadsf')
    result = collection.find_one(sort=[("batch", -1)])

    a=int(result['batch'])+1

    os.system("scrapy crawl ke -a arg="+str(a))
    os.system("scrapy crawl study163 -a arg="+str(a))
    os.system("scrapy crawl tianshan -a arg=" + str(a))
