""" Connect to twitch.tv chat channels, count emojis, and store the results in
    redis.
"""
import socket
import redis
from chat_client import TwitchChat
from chat_client.logger import make_logger
from chat_client.emoji_counter import EmojiCounter
from twitch_api_service import get_top_channel_names

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=0)
LOGGER = make_logger(__name__)

def main():
    top_channels = ['#' + name for name in get_top_channel_names(1000)]
    twitch_chat = TwitchChat(top_channels)
    while True:
        try:
            twitch_chat.login()
            counter = EmojiCounter(REDIS_CLIENT)
            while True:
                response = twitch_chat.get_message()
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
