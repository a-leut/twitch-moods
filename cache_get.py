import redis
from emoj import emojis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for emoji in emojis:
    print(emoji, r.get(emoji))
