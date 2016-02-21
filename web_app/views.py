from flask import render_template, current_app, Blueprint, jsonify
from twitch_api_service import get_emoticon_urls

api = Blueprint('api', __name__, url_prefix='/api/v1')
pages = Blueprint('pages', __name__, url_prefix='')

EMOJIS = get_emoticon_urls()

@api.route('/emoji_counts/', methods=['GET'])
def get_emoji_counts():
    results = {}
    for key in EMOJIS.keys():
        count = int(current_app.redis.hget("count", key))
        if count > 0:
            results[key] = {}
            results[key]["count"] = int(count)
            results[key]["url"] = str(current_app.redis.hget("url", key))
    return jsonify(results)

@pages.route('/')
def index():
    return render_template('index.html')
