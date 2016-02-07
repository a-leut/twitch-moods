import socket
from logger import get_logger
from emoji_counter import EmojiCounter
from twitch_irc_client import TwitchClient, SocketException

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
            logger = get_logger()
            logger.error('Fatal Exception: %s' % str(e))
            raise

if __name__ == '__main__':
    main()
