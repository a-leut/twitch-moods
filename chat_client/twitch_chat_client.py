import time
import socket
import redis
from chat_client import TwitchIRC, EmojiCounter, make_logger

class ChatClient(object):
    """ Reads twitch chat messages from given channel and updates counts of
        emoticons into redis with the EmojiCounter. Tries to reconnect to
        twitch if it loses connection
    """
    def __init__(self, channels, verbose=False):
        self._twitch = TwitchIRC(channels)
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._verbose = verbose

    def run(self):
        last_time = time.time()
        delay = 1
        while True:
            try:
                # Log in to twitch and reset emoji counts
                print("Joining chat channels...")
                self._twitch.login()
                print("Setting up redis counter...")
                counter = EmojiCounter(self._redis, verbose=self._verbose)
                print("Reading messages...")
                # Read twitch messages forever and update the counts
                while True:
                    response = self._twitch.get_message()
                    if response:
                        user, message = response
                        counter.update_emoji_count(message)
                        if self._verbose:
                            print('[Message] - %s: %s' % (user, message))
            except (socket.error, socket.timeout):
                # If lose connection to twitch try to restablish with delay
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
                logger = make_logger(__name__)
                logger.error('Fatal Exception: %s' % str(e))
                raise
