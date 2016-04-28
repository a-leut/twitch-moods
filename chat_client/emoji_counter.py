import time
from collections import Counter
from twitch_api_service import get_emoji_names_urls

class EmojiCounter(object):
    """ Counts emojis and stores the result in redis through the lifetime of
    the object.
    """
    def __init__(self, redis_connection):
        self.emojis, _ = get_emoji_names_urls()
        self._redis = redis_connection
        self._reset_redis()

    def update_emoji_count(self, message):
        tokens = message.split()
        emojis = [t for t in tokens if t in self.emojis]
        if emojis:
            emoji_counts = Counter(emojis)
            ts = time.time()
            for emoji, count in emoji_counts.most_common():
                self._add_key(ts, emoji, count)
            # update redis from counts
            for emoji in self.emojis:
                self._delete_old_keys(emoji, ts)
                self._update_count(emoji, ts)

    def _update_count(self, emoji, ts):
        count = self._redis.zcount('s_' + emoji, 0, ts)
        self._redis.set(emoji, count)
        if count > 0:
            print(emoji, count)

    def _delete_old_keys(self, emoji, ts, expire=60):
        self._redis.zremrangebyscore('s_' + emoji, 0, ts - expire)

    def _reset_redis(self):
        for emoji in self.emojis:
            self._redis.set(emoji, 0)

    def _add_key(self, time, emoji, count):
        """ Adds 'count' keys to the sorted set corresponding with 'emoji.'
            Unique names are given to the keys when 'count' > 1
        """
        print(time, emoji, count)
        if count == 1:
            self._redis.zadd('s_' + emoji, time, time)
        elif count > 1:
            # TODO: refactor to single call
            for n in range(count):
                self._redis.zadd('s_' + emoji, time - 0.001 * n, time)
