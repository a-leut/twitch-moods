import os
import re
import socket

NICK = os.environ.get('twitch_nick')
PASS = os.environ.get('twitch_key')
HOST = "irc.twitch.tv"
PORT = 6667

class TwitchIRC(object):
    """ Client for reading messages from twitch.tv chat. Connects to the chat
        server, joins some number of channels, and returns the next message
        from all the channels each time get_message is called.
    """
    def __init__(self, channels=[]):
        self.channels = channels
        self._con = None
        self._data = ""

    def login(self):
        self._connect_socket()
        self._con.send(bytes('PASS %s\r\n' % PASS, 'UTF-8'))
        self._con.send(bytes('NICK %s\r\n' % NICK, 'UTF-8'))
        for chan in self.channels:
            self._con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

    def get_message(self):
        """ Reads in new chat messages and returns the next message sent in
            chat and its sender.
        """
        new_data = self._con.recv(1024).decode('utf-8', 'ignore')
        self._data = self._data + new_data
        data_split = re.split(r"[~\r\n]+", self._data)
        self._data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    self._send_pong(line[1])
                    return self.get_message()

                if line[1] == 'PRIVMSG':
                    sender = self._get_sender(line[0])
                    message = self._get_message(line)
                    return sender, message

    def _connect_socket(self):
        con = socket.socket()
        con.connect((HOST, PORT))
        self._con = con

    def _send_pong(self, msg):
        self._con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def _join_channel(self, chan):
        self._con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

    def _get_sender(self, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        return result

    def _get_message(self, msg):
        result = ""
        i = 3
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        return result
