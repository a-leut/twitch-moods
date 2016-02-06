import redis
import socket
from collections import Counter
from twitch_client import TwitchClient, SocketException

def update_smiley_count(user, message, counter):
    pass

def main():
    twitch = TwitchClient(channel="#arteezy")

    while True:
        try:
            twitch.login()
            # todo: persist counter instead of reseting with client
            emoji_count = Counter()
            while True:
                response = twitch.get_message()
                if response:
                    user, message = response
                    update_smiley_count(user, message, emoji_count)
                    print(user, message)
        except (socket.error, socket.timeout):
            pass
            # todo: increase delay between reconnects
        except Exception:
            print('Fatal Exception')
            # todo: log?
            raise

if __name__ == '__main__':
    main()
