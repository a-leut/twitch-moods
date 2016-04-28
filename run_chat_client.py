""" Connect to twitch.tv chat channels, count emojis, and store the results in
    redis.
"""

from chat_client import ChatClient
from twitch_api_service import get_top_channel_names

def main():
    top_channels = get_top_channel_names(100)
    client = ChatClient(top_channels, verbose=True)
    client.run()

if __name__ == '__main__':
    main()