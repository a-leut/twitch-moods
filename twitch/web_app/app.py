import redis
from flask import Flask
from flask_cors import CORS

from twitch.web_app.views import api


def create_app(app_name='web_app'):
    app = Flask(app_name)
    CORS(app)

    app.config['DEBUG'] = True
    app.register_blueprint(api)
    app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    return app
