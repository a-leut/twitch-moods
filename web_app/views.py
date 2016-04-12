from flask import render_template, g, current_app, Blueprint, jsonify
from twitch_api_service import get_emoticon_urls
from .tasks import update_counts_from_redis

api = Blueprint('api', __name__, url_prefix='/api/v1')
pages = Blueprint('pages', __name__, url_prefix='')

EMOJIS = get_emoticon_urls()

def get_results():
    counts = current_app.redis.mget(EMOJIS.keys())
    counts = map(int, [c if c else 0 for c in counts])
    urls = map(str, EMOJIS.values())
    results = dict(zip(urls, counts))
    print(results)
    return jsonify(results)

@api.route('/emoji_counts/', methods=['GET'])
def get_emoji_counts():
    return get_results()

@pages.route('/')
def index():
    return render_template('index.html')
