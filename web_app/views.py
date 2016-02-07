from flask import render_template, current_app, Blueprint

views = Blueprint('views', __name__, url_prefix='')

@views.route('/')
def index():
    return render_template('index.html')
