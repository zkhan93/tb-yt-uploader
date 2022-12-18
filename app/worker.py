from celery import Celery

app = Celery('hello', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def hello():
    return 'hello world'
