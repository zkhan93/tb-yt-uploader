import logging
import logging.config

from celery import Celery
from celery.schedules import crontab
from app import create_app
from app.config import get_config
from app.tasks import *

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)
logger.info("info")
logger.debug("debug")
logger.error("error")

setting = get_config()
logger.debug("created settings")

logger.debug("creating app")
app = create_app(setting)
logger.debug("app created")



celery = Celery(__name__)
celery.conf.broker_url = setting.celery_broker_url
celery.conf.result_backend = setting.celery_result_backend

celery.conf.beat_schedule = {
    'refresh-token-every-30-min': {
        'task': 'app.tasks.check_auth',
        'schedule': crontab(minute='*'),
    },
}

