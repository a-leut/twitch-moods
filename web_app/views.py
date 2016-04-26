import numpy as np
from flask import current_app, Blueprint, jsonify
from twitch_api_service import get_emoji_names_urls

api = Blueprint('api', __name__, url_prefix='/api/v1')
names, urls = get_emoji_names_urls()

def get_results(cutoff=40):
    """ Returns json form emoji counts from redis for count in the top `cutoff`
        percentile and above
    """
    counts = current_app.redis.mget(names)
    n_counts = np.array([int(c) for c in counts])
    n_counts = n_counts[np.nonzero(n_counts)]  # remove 0s
    percentile = np.percentile(n_counts, cutoff)
    results = {}
    for i, count in enumerate(counts):
        if count and int(count) > percentile:
            results[urls[i]] = int(count)
    return jsonify(results)

@api.route('/emoji_counts/', methods=['GET'])
def get_emoji_counts():
    return get_results()
