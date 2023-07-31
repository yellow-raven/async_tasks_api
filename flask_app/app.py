from flask import Flask
from waitress import serve
from celery import Celery

app = Flask(__name__)

celery = Celery(
    'tasks', 
    broker='amqp://admin:mypass@rabbit:5672//', 
    backend='redis://redis:6379/0'
)

@app.route('/task/<task_name>', methods=['POST'])
def call_method(task_name):
    app.logger.info(f"Invoking Method {task_name}")
    #queue name in task folder.function name
    r = celery.send_task(f'tasks.{task_name}', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id

@app.route('/task/status/<task_id>')
def get_status(task_id):
    status = celery.AsyncResult(task_id)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)

@app.route('/task/result/<task_id>')
def task_result(task_id):
    result = celery.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

if __name__ == '__main__':
    serve(app,host = '0.0.0.0',port = 5001)