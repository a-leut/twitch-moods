""" Counts emojis and stores the result in redis through the lifetime of the
    object.
"""
import redis
from collections import Counter
from emoj import emojis

class EmojiCounter(object):
    def __init__(self):
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._reset_redis_count()
        self.counter = Counter()

    def update_emoji_count(self, message):
        for token in message.split():
            updated_emojis = []
            if token in emojis:
                self.counter[token] += 1
                if token not in updated_emojis:
                    updated_emojis.append(token)
            self._update_redis(updated_emojis)

    def _reset_redis_count(self):
        for emoji in emojis:
            self._redis.set(emoji, 0)

    def _update_redis(self, updated):
        for emoji in updated:
            self._redis.set(emoji, self.counter[emoji])


