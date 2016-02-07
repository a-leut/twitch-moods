from flask import Flask
from .views import views

def create_app(config=None, app_name='twitch_web_app'):
    app = Flask(app_name)

    app.register_blueprint(views)

    return app
