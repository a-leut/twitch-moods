CHAN = "#arteezy"

from twitch_client import TwitchClient, SocketException

def print_message(user, message):
    print(user, message)

def main():
    twitch = TwitchClient(channel="#arteezy")
    twitch.add_observer(print_message)

    while True:
        try:
            twitch.login()
            twitch.read_messages()
        except SocketException:
            pass
            # todo: increase delay between reconnects
        except Exception:
            print('Fatal Exception')
            # TODO: log
            raise


if __name__ == '__main__':
    main()
