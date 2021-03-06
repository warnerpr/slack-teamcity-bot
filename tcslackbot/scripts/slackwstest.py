""" confirm we can talk web sockets to slack """

from __future__ import print_function

from twisted.internet import reactor
from tcslackbot.utils import slacktoken
from tcslackbot.utils import slackwstransport


def main():
    token = slacktoken.get_token()
    wsman = slackwstransport.SlackWebSocketManager(token, lambda _m: print(_m))
    reactor.callWhenRunning(wsman.connect)
    reactor.run()


if __name__ == '__main__':
    main()
