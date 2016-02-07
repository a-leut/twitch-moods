import socket

from irc_client.logger import get_logger
from irc_client.emoji_counter import EmojiCounter
from irc_client.client import TwitchClient

channels = ['#moonducktv']

def main():
    twitch = TwitchClient(channels)
    while True:
        try:
            twitch.login()
            counter = EmojiCounter()
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
            logger = get_logger(__name__)
            logger.error('Fatal Exception: %s' % str(e))
            raise

if __name__ == '__main__':
    main()
