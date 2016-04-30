import time
from collections import Counter
from twitch_api_service import get_emoji_names_urls

class EmojiCounter(object):
    """ Counts emojis and stores the result in redis through the lifetime of
        the object.

        Timestamps of emojis are stored in sorted sets named "s_[emoji]" and
        counts of these timestamps are stored in keys named "[emoji]."
    """
    BUFFER_LIMIT = 20

    def __init__(self, redis_connection, verbose=False):
        self.emojis, _ = get_emoji_names_urls()
        self._redis = redis_connection
        self._reset_redis()
        self._messages = []
        # Set of emojis for which there are non-empty sorted sets of timestamps
        self._known_emojis = set()
        self._verbose = verbose

    def update_emoji_count(self, message):
        """ Adds message to message buffer. Processes and resets the buffer
            once we reach a certain number of messages.
        """
        self._messages.append(message)
        if len(self._messages) > EmojiCounter.BUFFER_LIMIT:
            self.process_messages()
            self._messages = []

    def process_messages(self):
        """ Adds keys to emoji sorted sets for each emoji in message buffer
            and then updates count keys in redis from sorted sets
        """
        token_arrays = [m.split() for m in self._messages]
        tokens = [item for sublist in token_arrays for item in sublist]
        emojis = [t for t in tokens if t in self.emojis]
        if emojis:
            emoji_counts = Counter(emojis)
            ts = time.time()
            for emoji, count in emoji_counts.most_common():
                self._known_emojis.add(emoji)
                self._add_timestamp(ts, emoji, count)
            # Update count keys from sorted sets
            to_remove = set()
            for emoji in self._known_emojis:
                self._delete_old_timestamps(emoji, ts)
                count = self._update_count_key(emoji, ts)
                to_remove.add(emoji)
            self._known_emojis.difference_update(to_remove)

    def _update_count_key(self, emoji, ts):
        count = self._redis.zcount('s_' + emoji, 0, ts)
        self._redis.set(emoji, count)
        if self._verbose:
            print('Set %s to %s' % (emoji, count))
        return count

    def _delete_old_timestamps(self, emoji, ts, expire=60):
        self._redis.zremrangebyscore('s_' + emoji, 0, ts - expire)

    def _reset_redis(self):
        for emoji in self.emojis:
            self._redis.zremrangebyrank('s_' + emoji, -1, 0)
            self._redis.set(emoji, 0)

    def _add_timestamp(self, time, emoji, count):
        """ Adds 'count' keys to the sorted set corresponding with 'emoji.'
            Unique names are given to the keys when 'count' > 1
        """
        if count == 1:
            self._redis.zadd('s_' + emoji, time, time)
        elif count > 1:
            # TODO: refactor to single redis call
            for n in range(count):
                unique_time = time + (0.0000001 * n)
                self._redis.zadd('s_' + emoji, unique_time, unique_time)
        if self._verbose:
            print('Added %s to s_%s %s times' %(time, emoji, count))

