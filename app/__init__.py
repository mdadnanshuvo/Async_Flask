from flask import Flask
from celery import Celery
from redis import Redis
from app.tasks import make_celery, register_tasks


app = Flask(__name__)
redis = Redis(host='redis', port=6379)

def create_app():
    app = Flask(__name__)
    
    
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:/6379/10'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:/6379/10'
    

    make_celery(app)

    register_tasks()

    from app.routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app

