import time
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

hard_worker = Celery(
       'worker', 
       broker='amqp://admin:mypass@rabbit:5672//', 
       backend='redis://redis:6379/0'
    )

# Configure Celery to use threads for concurrency
hard_worker.conf.update(
    task_concurrency=4,  # Use 4 threads for concurrency
    worker_prefetch_multiplier=1  # Prefetch one task at a time
)

@hard_worker.task()
def count(n):
    logger.info('Got Request - Starting work ')
    counting_list=[]
    for i in range(n):
        counting_list.add(i+1)
    logger.info('Work Finished ')
    return counting_list

@hard_worker.task()
def prime(n):
    logger.info('Got Request - Starting work ')
    prime = list()
    sieve = [True] * (n+1)
    for p in range(2, n+1):
        if (sieve[p] and sieve[p]%2==1):
            prime.append(p)
            for i in range(p, n+1, p):
                sieve[i] = False
    logger.info('Work Finished ')
    return prime

@hard_worker.task()
def fibo(n):
    logger.info('Got Request - Starting work ')
    fibo = []
    a,b = 0,1
    while b < n:
        a,b = b,a+b
        fibo.append(a)
    logger.info('Work Finished ')
    return fibo