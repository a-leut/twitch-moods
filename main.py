import socket
from collections import Counter
from emoj import emojis
from twitch_client import TwitchClient, SocketException

channels = ['#voyboy', '#stonedyooda', '#c9sneaky', '#trick2g']

def update_smiley_count(user, message, counter):
    # todo: parse emoji
    for token in message.split():
        updated = []
        if token in emojis:
            counter[token] += 1
            if token not in updated:
                updated.append(token)

def main():
    twitch = TwitchClient(channels)

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
        except (socket.error, socket.timeout):
            pass
            # todo: increase delay between reconnects
        except Exception:
            print('Fatal Exception')
            # todo: log?
            raise

if __name__ == '__main__':
    main()
