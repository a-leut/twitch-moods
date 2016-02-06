#!/usr/bin/env python3

import re
import socket

NICK = "deep_fart"
PASS = "oauth:05m35xbppp0zgt71nymghqgmaput8x"
HOST = "irc.twitch.tv"
PORT = 6667

class SocketException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TwitchClient(object):
    """ Client for reading messages from twitch.tv chat. Connects to the chat
        server, joins some number of channels, and updates observer functions
        when messages are posted to the channel(s).

        TODO:
        Multiple channels
        Refactor to asyncio
    """
    def __init__(self, channel=None):
        self.channel = channel
        self._con = None
        self.obs = []

    def add_observer(self, observer):
        if observer not in self.obs:
            self.obs.append(observer)

    def remove_observer(self, observer):
        self.obs.remove(observer)

    def login(self):
        self._connect_socket()
        self._con.send(bytes('PASS %s\r\n' % PASS, 'UTF-8'))
        self._con.send(bytes('NICK %s\r\n' % NICK, 'UTF-8'))
        self._con.send(bytes('JOIN %s\r\n' % self.channel, 'UTF-8'))

    def _notify_observers(self, *args, **kwargs):
        for observer in self.obs:
            observer(*args, **kwargs)

    def read_messages(self):
        data = ""
        while True:
            try:
                data = data+self._con.recv(1024).decode('UTF-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()

                for line in data_split:
                    line = str.rstrip(line)
                    line = str.split(line)

                    if len(line) >= 1:
                        if line[0] == 'PING':
                            self.send_pong(line[1])

                        if line[1] == 'PRIVMSG':
                            sender = self._get_sender(line[0])
                            message = self._get_message(line)
                            self._notify_observers(sender, message)

            except socket.error:
                # todo: log?
                raise SocketException("Socket died")

            except socket.timeout:
                raise SocketException("Socket timout")

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
