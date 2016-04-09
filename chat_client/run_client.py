""" Connect to twitch.tv chat channels, count emojis, and store the results in
    redis.
"""
import time
import socket
import redis
from chat_client import TwitchChat, EmojiCounter, make_logger
from twitch_api_service import get_top_channel_names

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=0)
LOGGER = make_logger(__name__)
VERBOSE = False

def main():
    top_channels = ['#' + name for name in get_top_channel_names(100)]
    twitch = TwitchChat(top_channels)
    last_time = time.time()
    delay = 1
    while True:
        try:
            # log in to twitch and reset emoji counts
            twitch.login()
            counter = EmojiCounter(REDIS_CLIENT)
            # read twitch messages forever and update the counts
            while True:
                response = twitch.get_message()
                if response:
                    user, message = response
                    counter.update_emoji_count(message)
                    if VERBOSE:
                        print(user, message)
        except (socket.error, socket.timeout):
            # if lose connection to twitch try to restablish with delay
            cur_time = time.time()
            print('Timeout: lost connection')
            if cur_time - last_time < 10:
                time.sleep(delay)
                delay *= 2
            else:
                delay = 1
            last_time = cur_time
        except Exception as e:
            print('Fatal Exception')
            LOGGER.error('Fatal Exception: %s' % str(e))
            raise

if __name__ == '__main__':
    main()
