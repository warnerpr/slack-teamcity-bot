""" confirm we can talk web sockets to slack """

from __future__ import print_function
import slacktoken
import requests
from urlparse import urlparse

from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory, connectWS)


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

def ask_for_websocket(token):
    """ ask the slack server for a websocket,
        return the WS URI assuming we get one """
    url = 'https://slack.com/api/rtm.start'
    resp = requests.get(url, params={'token': token})
    return resp.json()['url']

def main():
    token = slacktoken.get_token()
    ws_url = ask_for_websocket(token)

    from twisted.internet import reactor, ssl

    factory = WebSocketClientFactory(ws_url)
    factory.protocol = MyClientProtocol

    if factory.isSecure:
        contextFactory = ssl.ClientContextFactory()
    else:
        contextFactory = None
    connectWS(factory, contextFactory)

    reactor.run()


if __name__ == '__main__':
    main()

