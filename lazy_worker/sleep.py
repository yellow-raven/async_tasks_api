import time
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

lazy_worker = Celery(
       'worker', 
       broker='amqp://admin:mypass@rabbit:5672//', 
       backend='redis://redis:6379/0'
    )

@lazy_worker.task()
def sleep(duration):
    logger.info('Got Request - Starting work ')
    time.sleep(duration)
    logger.info('Work Finished ')
    return f"Slept for {duration} seconds."