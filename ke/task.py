# task.py
from celery import Celery
import os
import pymongo
from celery.schedules import crontab

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['ke']
collection = db['ke']

app = Celery('task', backend='redis://localhost', broker='redis://localhost//')

#to do 每天执行
#to do flower

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    #sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(crontab(hour=11, minute=5, day_of_week=0),test.s(),)

    sender.add_periodic_task(crontab(hour=9, minute=35),task_ke.s(),)

@app.task
def test():
    print('2323')

@app.task()
def task_ke( ):
    a=0
    print('asdfadsfadsfadsf')
    result = collection.find_one(sort=[("batch", -1)])

    arg=int(result['batch'])+1

    os.system("scrapy crawl ke -a arg="+a)
    os.system("scrapy crawl study163 -a arg="+a)


if __name__ == "__main__":
    app.start()