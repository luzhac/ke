# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
#CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
CELERY_TIMEZONE='UTC'
# import
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2',
    'celery_app.task3'
)
# schedules
CELERYBEAT_SCHEDULE = {

    'multiply-at-some-time': {
        'task': 'celery_app.task3.crawl1',
        'schedule': crontab(hour=11, minute=10),    
        'args': ()                            # 任务函数参数
    }
}