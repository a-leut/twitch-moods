""" Counts emojis and stores the result in redis through the lifetime of the
    object.
"""
from collections import Counter
from twitch_api_service import get_emoticon_urls

class EmojiCounter(object):
    def __init__(self, redis_connection):
        self.counter = Counter()
        self.emojis = get_emoticon_urls()
        self._redis = redis_connection
        self._reset_redis()

    def update_emoji_count(self, message):
        for token in message.split():
            updated_emoji_keys = []
            if token in self.emojis.keys():
                self.counter[token] += 1
                if token not in updated_emoji_keys:
                    updated_emoji_keys.append(token)
            self._update_redis(updated_emoji_keys)

    def _reset_redis(self):
        for key in self.emojis.keys():
            self._redis.hset("url", key, self.emojis[key])
            self._redis.hset("count", key, 0)

    def _update_redis(self, updated_emoji_keys):
        for key in updated_emoji_keys:
            self._redis.hset("count", key, self.counter[key])
