""" Connect to twitch.tv chat channels, count emojis, and store the results in
    redis.
"""
import socket
import redis
from irc_client.logger import make_logger
from irc_client.emoji_counter import EmojiCounter
from irc_client.client import TwitchClient

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=0)
CHANNELS = ['#arteezy']
LOGGER = make_logger(__name__)

def main():
    twitch = TwitchClient(CHANNELS)
    while True:
        try:
            twitch.login()
            counter = EmojiCounter(REDIS_CLIENT)
            while True:
                response = twitch.get_message()
                if response:
                    user, message = response
                    print(user, message)
                    counter.update_emoji_count(message)
        except (socket.error, socket.timeout):
            pass
        except Exception as e:
            print('Fatal Exception')
            LOGGER.error('Fatal Exception: %s' % str(e))
            raise

if __name__ == '__main__':
    main()
