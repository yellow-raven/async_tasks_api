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
def sleep(parameters):
    logger.info('Got Request - Starting work ')
    time.sleep(parameters['duration'])
    logger.info('Work Finished ')
    return f"Slept for {parameters['duration']} seconds."

@celery.task()
def fibo(parameters):
    logger.info('Got Request - Starting work ')
    n=parameters['iter']
    fibo = []
    a,b = 0,1
    while b < n:
        a,b = b,a+b
        fibo.append(a)
    logger.info('Work Finished ')
    return fibo