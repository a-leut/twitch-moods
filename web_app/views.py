from flask import render_template, g, current_app, Blueprint, jsonify
from twitch_api_service import get_emoji_names_urls
from .tasks import update_counts_from_redis

api = Blueprint('api', __name__, url_prefix='/api/v1')
pages = Blueprint('pages', __name__, url_prefix='')

names, urls = get_emoji_names_urls()

def get_results():
    results = {}
    counts = current_app.redis.mget(names)
    for i, count in enumerate(counts):
        if count and int(count) > 0:
            results[urls[i]] = int(count)
    return jsonify(results)

@api.route('/emoji_counts/', methods=['GET'])
def get_emoji_counts():
    return get_results()

@pages.route('/')
def index():
    return render_template('index.html')
