import numpy as np
from flask import current_app, Blueprint, jsonify

from twitch.api_service import get_emoji_names_urls

api = Blueprint('api', __name__, url_prefix='/api/v1')
names, urls = get_emoji_names_urls()

def get_results(cutoff=None):
    """ Returns json of emoji counts from redis for counts in the top
        'cutoff' percentile of total counts and above
    """
    counts = current_app.redis.mget(names)
    results = {}
    if cutoff:
        # Return results in the top percentile cutoff
        n_counts = np.array([int(c) for c in counts])
        n_counts = n_counts[np.nonzero(n_counts)]
        percentile = np.percentile(n_counts, cutoff)
        for i, count in enumerate(counts):
            if count and int(count) >= percentile:
                results[urls[i]] = int(count)
    else:
        for i, count in enumerate(counts):
            if count and int(count):
                results[urls[i]] = int(count)
    return jsonify(results)

@api.route('/emoji_counts/', methods=['GET'])
def get_emoji_counts():
    return get_results()
