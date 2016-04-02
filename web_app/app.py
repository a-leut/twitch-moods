import redis
from flask import Flask
from celery import Celery
from .views import pages, api

def create_app(app_name='web_app'):
    app = Flask(app_name)

    # Config
    app.config['DEBUG'] = True
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    # Blueprints
    app.register_blueprint(pages)
    app.register_blueprint(api)

    # Libraries
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    app.celery = celery
    app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    return app
