from celery import Celery

celery = None


def make_celery(app):
    global celery
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
   
    )
    celery.conf.update(app.config)
    return celery




def register_tasks():
    global celery

    @celery.task
    def long_running_task(data):
        import time
        time.sleep(10)
        return {"Message ": "Task completed succesfully", "input":data}