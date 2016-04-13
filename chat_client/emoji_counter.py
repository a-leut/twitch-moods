from collections import Counter
from twitch_api_service import get_emoji_names_urls

class EmojiCounter(object):
    """ Counts emojis and stores the result in redis through the lifetime of
    the object.
    """
    def __init__(self, redis_connection):
        self.counter = Counter()
        self._emojis, _ = get_emoji_names_urls()
        self._redis = redis_connection
        self._reset_redis()

    def update_emoji_count(self, message):
        for token in message.split():
            updated_emoji_keys = []
            if token in self._emojis:
                self.counter[token] += 1
                if token not in updated_emoji_keys:
                    updated_emoji_keys.append(token)
            self._update_redis(updated_emoji_keys)

    def _reset_redis(self):
        for key in self._emojis:
            self._redis.set(key, 0)

    def _update_redis(self, updated_emoji_keys):
        for key in updated_emoji_keys:
            self._redis.set(key, self.counter[key])
