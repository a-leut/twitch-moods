import redis
from flask import Flask
from .views import pages, api

def create_app(app_name='twitch_web_app'):
    app = Flask(app_name)

    app.config['DEBUG'] = True

    app.register_blueprint(pages)
    app.register_blueprint(api)
    app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    return app
