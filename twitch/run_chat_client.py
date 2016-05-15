""" Connect to twitch.tv chat channels, count emojis, and store the results in
    redis.
"""

from twitch.chat_client import ChatClient
from twitch.api_service import get_top_channel_names

def main():
    top_channels = get_top_channel_names(100)

    client = ChatClient(top_channels, verbose=False)
    client.run()

if __name__ == '__main__':
    main()
