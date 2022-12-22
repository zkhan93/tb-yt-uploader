from celery import Celery
from celery.schedules import crontab

app = Celery('hello', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
app.conf.beat_schedule = {
    'refresh-token-every-30-min': {
        'task': 'app.celery.tasks.all.check_auth',
        'schedule': crontab(),
    },
}
from app.celery.tasks.all import *
