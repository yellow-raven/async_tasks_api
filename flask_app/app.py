from flask import Flask, request
from waitress import serve
from celery import Celery
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

app = Flask(__name__)

worker = Celery(
    'worker', 
    broker='amqp://admin:mypass@rabbit:5672//', 
    backend='redis://redis:6379/0'
)

@app.route('/sleep', methods=['POST'])
def sleep():
    app.logger.info(f"Invoking Method Sleep")
    #queue name in task folder.function name
    duration = request.form.get("duration")
    r = worker.send_task('sleep.sleep', 
                         kwargs={'duration': {duration}},
                         queue="lazy"
                        )
    app.logger.info(r.backend)
    return r.id

@app.route('/sleep/status/<task_id>')
def get_sleep_status(task_id):
    status = worker.AsyncResult(task_id)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)

@app.route('/sleep/result/<task_id>')
def task_sleep_result(task_id):
    result = worker.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

@app.route('/task/<task_name>', methods=['POST'])
def call_method(task_name):
    app.logger.info(f"Invoking Method {task_name}")
    #queue name in task folder.function name
    number = request.form.get("parameter")
    r = worker.send_task(f'tasks.{task_name}', 
                         kwargs={'n': {number}},
                         queue="hard"
                        )
    app.logger.info(r.backend)
    return r.id

@app.route('/task/status/<task_id>')
def get_status(task_id):
    status = worker.AsyncResult(task_id)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)

@app.route('/task/result/<task_id>')
def task_result(task_id):
    result = worker.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

if __name__ == '__main__':
    serve(app,host = '0.0.0.0',port = 5001)