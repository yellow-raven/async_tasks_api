import time
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery = Celery(
       'worker', 
       broker='amqp://admin:mypass@rabbit:5672//', 
       backend='redis://redis:6379/0'
    )

@celery.task()
def long_sleep(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(20)
    logger.info('Work Finished ')
    return x + y

@celery.task()
def short_sleep(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(1)
    logger.info('Work Finished ')
    return x + y