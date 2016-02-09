from flask import render_template, current_app, Blueprint, jsonify
from emoj import emojis

views = Blueprint('views', __name__, url_prefix='')

@views.route('/counts/', methods=['GET'])
def get_emoji_counts():
    counts = {}
    for emoji in emojis:
        counts[emoji] = int(current_app.redis.get(emoji))
    return jsonify(counts)

@views.route('/')
def index():
    return render_template('index.html')
